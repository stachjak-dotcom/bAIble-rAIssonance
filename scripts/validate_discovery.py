#!/usr/bin/env python3
"""Validate bAIble discovery, vocabulary and publication integrity.

Checks are grouped so a failure says which promise broke:
- discovery: required files, graph resources, routing/view hints, manifest, llms.txt links;
- vocabulary: graph predicates and node types, failure-mode coverage, blocker lists;
- repository: every active document is discoverable, relative links resolve, no case-only path collisions;
- publication: no private run identifiers or private project names in the public repository;
  the list of private names is supplied from outside the repository (BAIBLE_PRIVATE_NAMES).
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Identity of this repository; llms.txt absolute links must point here.
REPOSITORY = "stachjak-dotcom/bAIble-rAIssonance"
BRANCH = "main"

REQUIRED = [
    "README.md", "AGENTS.md", "llms.txt", "BIBLE.md", "OPERATING.md", "ECOSYSTEM.md",
    "BOUNDARY.md", "ECOSYSTEM_GRAPH.json", "AI_CONTEXT_MANIFEST.json", "vocabulary.json",
]

# Public repository must not carry private runtime identifiers (GitHub Actions run ids)
# or names of private pilot projects. The list of names is never stored here (see private_names).
RUN_ID = re.compile(r"(?<![\w/.-])3\d{10}(?![\w-])")
PRIVATE_NAMES_ENV = "BAIBLE_PRIVATE_NAMES"
REQUIRE_FLAG = "--require-private-names"


def private_names() -> list[str] | None:
    """Private project names come from outside the public repository (e.g. a CI secret).

    Returns None when the list was not provided, so callers can report the check as
    NOT PERFORMED instead of passed. Entries are separated by newlines or commas.
    """
    raw = os.environ.get(PRIVATE_NAMES_ENV, "")
    names = [n.strip() for n in re.split(r"[\n,]", raw) if n.strip()]
    return names or None

# Documents that are adapters, history or generated output are not required in the manifest.
NOT_IN_MANIFEST = {"README.md", "AGENTS.md"}


def load_json(path: pathlib.Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report any parse problem
        errors.append(f"invalid {path.name}: {exc}")
        return {}


def tracked_files() -> list[str]:
    # stderr is discarded, not inherited: git diagnostics may contain paths with listed names
    # and would reach the public log before redact() can see them (G-028).
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        return [line for line in out.splitlines() if line]
    except Exception:  # noqa: BLE001 - outside git, fall back to the tree
        return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]


def check_discovery(graph: dict, manifest: dict, errors: list[str]) -> None:
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            errors.append(f"discovery: missing required file {path}")

    node_ids = {n.get("id") for n in graph.get("nodes", [])}
    for node in graph.get("nodes", []):
        for resource in node.get("resources", []):
            if not (ROOT / resource).is_file():
                errors.append(f"discovery: node {node.get('id')} references missing resource {resource}")
    for view, refs in graph.get("view_hints", {}).items():
        for ref in refs:
            if ref not in node_ids:
                errors.append(f"discovery: view_hints.{view} references missing node {ref}")
    for route, spec in graph.get("routing_hints", {}).items():
        for ref in spec.get("nodes", []):
            if ref not in node_ids:
                errors.append(f"discovery: routing_hints.{route} references missing node {ref}")
        for resource in spec.get("resources", []):
            if not (ROOT / resource).is_file():
                errors.append(f"discovery: routing_hints.{route} references missing resource {resource}")
    for rel in graph.get("relations", []):
        for end in ("subject", "object"):
            if rel.get(end) not in node_ids:
                errors.append(f"discovery: relation {rel.get('id')} {end} {rel.get(end)} is not a node")

    for profile, files in manifest.get("profiles", {}).items():
        seen: set[str] = set()
        for path in files:
            if path in seen:
                errors.append(f"discovery: manifest profile {profile} duplicates {path}")
            seen.add(path)
            if not (ROOT / path).is_file():
                errors.append(f"discovery: manifest profile {profile} references missing {path}")

    check_llms(errors)


def check_llms(errors: list[str]) -> None:
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8") if (ROOT / "llms.txt").is_file() else ""
    own = f"https://raw.githubusercontent.com/{REPOSITORY}/{BRANCH}/"
    for url in re.findall(r"https://raw\.githubusercontent\.com/[^\s)]+", llms):
        if not url.startswith(own):
            errors.append(f"discovery: llms.txt points outside this repository: {url}")
            continue
        path = url[len(own):]
        parts = path.split("/")
        if not path or path.startswith("/") or "" in parts or ".." in parts:
            errors.append(f"discovery: llms.txt points to an invalid repository path {path}")
            continue
        target = (ROOT / path).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            errors.append(f"discovery: llms.txt points outside the repository tree {path}")
        elif not target.is_file():
            errors.append(f"discovery: llms.txt points to missing repository path {path}")


def check_vocabulary(graph: dict, vocab: dict, errors: list[str]) -> None:
    predicates = {p for group in vocab.get("relations", {}).values() for p in group}
    for rel in graph.get("relations", []):
        if rel.get("predicate") not in predicates:
            errors.append(f"vocabulary: relation {rel.get('id')} uses predicate {rel.get('predicate')!r} not in vocabulary.json")
    node_classes = set(vocab.get("node_classes", []))
    for node in graph.get("nodes", []):
        if node.get("type") not in node_classes:
            errors.append(f"vocabulary: node {node.get('id')} has type {node.get('type')!r} not in vocabulary.json")

    failure_doc = ROOT / "FAILURE_MODES.md"
    if failure_doc.is_file():
        modes = re.findall(r"^## (.+)$", failure_doc.read_text(encoding="utf-8"), re.M)
        risk_labels = {n.get("label") for n in graph.get("nodes", []) if n.get("type") == "risk"}
        for mode in modes:
            if mode.strip() not in risk_labels:
                errors.append(f"vocabulary: failure mode {mode!r} has no risk node in ECOSYSTEM_GRAPH.json")

    # Any bullet list that enumerates blocking states must use only the canonical states.
    allowed = set(vocab.get("blocking_states", {})) | set(vocab.get("terminal_states", {}))
    for doc in active_documents():
        lines = doc.read_text(encoding="utf-8").splitlines()
        block: list[str] = []
        for line in lines + [""]:
            m = re.match(r"^- `?([A-Z][A-Z_]+[A-Z])`?[,.]?\s*(?:—.*)?$", line.strip())
            if m:
                block.append(m.group(1))
                continue
            if "MISSING_CONTEXT" in block:
                for state in block:
                    if state not in allowed:
                        errors.append(f"vocabulary: {doc.name} lists blocking state {state} not in vocabulary.json")
            block = []


def active_documents() -> list[pathlib.Path]:
    return [p for p in sorted(ROOT.glob("*.md"))]


def check_repository(manifest: dict, files: list[str], errors: list[str]) -> None:
    listed = {p for group in manifest.get("profiles", {}).values() for p in group}
    for doc in active_documents():
        if doc.name not in listed and doc.name not in NOT_IN_MANIFEST:
            errors.append(f"repository: {doc.name} is an active document but not in AI_CONTEXT_MANIFEST.json")
    for doc in active_documents() + [ROOT / "history" / "README.md"]:
        if not doc.is_file():
            continue
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", doc.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (doc.parent / target).exists():
                errors.append(f"repository: {doc.relative_to(ROOT)} links to missing {target}")
    lowered: dict[str, str] = {}
    for path in files:
        key = path.lower()
        if key in lowered and lowered[key] != path:
            errors.append(f"repository: {path} and {lowered[key]} differ only by letter case")
        lowered[key] = path


def check_publication(files: list[str], errors: list[str], names: list[str] | None) -> None:
    """Report only the path and the category; never echo the matched value into logs."""
    for path in files:
        if not path.endswith((".md", ".json", ".txt", ".yml", ".py")):
            continue
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        if RUN_ID.search(text):
            errors.append(f"publication: {path} contains a private run id")
        # Case-insensitive, the same way redact() matches (G-028).
        lowered = text.lower()
        if names and any(name.lower() in lowered for name in names):
            errors.append(f"publication: {path} names a listed private project")


def redact(text: str, names: list[str] | None) -> str:
    """Last line of defence: no listed name and no run id may reach any output (logs are public)."""
    text = RUN_ID.sub("[REDACTED-RUN-ID]", text)
    for name in sorted(names or [], key=len, reverse=True):
        text = re.sub(re.escape(name), "[REDACTED]", text, flags=re.IGNORECASE)
    return text


def run(argv: list[str], names: list[str] | None) -> tuple[int, list[str]]:
    require_names = REQUIRE_FLAG in argv
    errors: list[str] = []
    graph = load_json(ROOT / "ECOSYSTEM_GRAPH.json", errors)
    manifest = load_json(ROOT / "AI_CONTEXT_MANIFEST.json", errors)
    vocab = load_json(ROOT / "vocabulary.json", errors)
    files = tracked_files()

    check_discovery(graph, manifest, errors)
    check_vocabulary(graph, vocab, errors)
    check_repository(manifest, files, errors)
    check_publication(files, errors, names)
    if names is None and require_names:
        errors.append(f"publication: private-name list required ({REQUIRE_FLAG}) but {PRIVATE_NAMES_ENV} is not provided")

    if errors:
        return 1, ["Validation FAILED:"] + [f"- {err}" for err in errors]
    if names is None:
        return 0, ["Validation passed: discovery, vocabulary, repository and run-id checks. "
                   f"Private-name check NOT PERFORMED ({PRIVATE_NAMES_ENV} not provided); publication is NOT fully verified."]
    return 0, ["Validation passed: discovery, vocabulary, repository and publication checks."]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    names = private_names()
    try:
        code, lines = run(argv, names)
    except Exception as exc:  # noqa: BLE001 - never let a traceback print unredacted data
        print(redact(f"Validation ERROR: {type(exc).__name__}: {exc}", names), file=sys.stderr)
        return 2
    stream = sys.stderr if code else sys.stdout
    for line in lines:
        print(redact(line, names), file=stream)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
