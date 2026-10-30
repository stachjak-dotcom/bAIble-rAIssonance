#!/usr/bin/env python3
"""Generate a single-file bAIble AI context bundle.

The bundle records its planned repository and local git checkpoint; it does not claim
a verified source revision (see source_identity).

The output is a transport artifact, not a canonical source. Edit source files,
not the generated bundle.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "AI_CONTEXT_MANIFEST.json"
PLANNED_REPOSITORY = "stachjak-dotcom/bAIble-rAIssonance"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()


def source_identity() -> list[str]:
    """Describe the sources without claiming more than this tool checks.

    This preparatory version never names a source revision: a local HEAD does not prove
    that every file read into the bundle has that content, and the planned repository is
    not verified here. Binding a published bundle to its sources is a pre-publication check.
    """
    lines = [
        f"- planned repository: {PLANNED_REPOSITORY} (target; not verified by this tool)",
        "- source revision: UNKNOWN (not established by this tool)",
    ]
    try:
        top = pathlib.Path(git("rev-parse", "--show-toplevel")).resolve()
        head = git("rev-parse", "HEAD")
    except Exception:
        return lines
    where = "" if top == ROOT else f"; sources under subpath {ROOT.relative_to(top)}"
    return lines + [f"- local git HEAD: {head} (local checkpoint, not a fingerprint of the files read{where})"]


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def selected_files(manifest: dict, profile: str) -> list[str]:
    core = manifest["profiles"]["core"]
    if profile == "core":
        return core
    if profile == "full":
        return core + manifest["profiles"].get("reference", [])
    raise ValueError(f"Unsupported profile: {profile}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=["core", "full"], default="core")
    parser.add_argument("--output", default="dist/BAIBLE_AI_CONTEXT.md")
    args = parser.parse_args()

    manifest = load_manifest()
    files = selected_files(manifest, args.profile)

    missing = [p for p in files if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit("Missing source files: " + ", ".join(missing))

    generated_at = datetime.now(timezone.utc).isoformat()
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        "# bAIble-rAIssonance — Generated AI Context Bundle",
        "",
        "> GENERATED TRANSPORT ARTIFACT — DO NOT EDIT AS A CANONICAL SOURCE.",
        "> Canonical meaning remains in the source files listed below.",
        "",
        f"- profile: {args.profile}",
        *source_identity(),
        f"- generated at: {generated_at}",
        "- manifest: AI_CONTEXT_MANIFEST.json",
        "",
        "Core distinction:",
        "",
        "DISCOVERABLE != LOADED != ACTIVE != AUTHORIZED",
        "",
        "## Included source files",
        "",
    ]
    parts.extend(f"- {p}" for p in files)
    parts.extend(["", "---", ""])

    for path in files:
        text = (ROOT / path).read_text(encoding="utf-8").rstrip()
        parts.extend([
            f"# SOURCE: {path}",
            "",
            text,
            "",
            "---",
            "",
        ])

    out.write_text("\n".join(parts), encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
