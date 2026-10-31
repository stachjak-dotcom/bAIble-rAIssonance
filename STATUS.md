# bAIble-rAIssonance — Status

What is built, tested and verified, what remains open, and the self-audit before any release. Columns follow the ladder for work we build ([VERIFICATION.md](VERIFICATION.md)): DESIGNED → BUILT → TESTED → VERIFIED → INTEGRATED.

## This version

This candidate is being prepared from bAIble v2 at revision `80b7262de738d5fdb6e07fe82f31aff6c77ce999`. The intended transfer preserves meaning except where a change is explicitly recorded. Repository identity and addresses are being adapted; preparation and verification of the complete candidate are not finished.

- **Release claim: none yet.** The first claim is made only after the candidate has been checked for content and links, publication scope, and one full entry by a fresh AI with a record of what its tools actually returned.
- Evidence gathered for bAIble v2 does not transfer automatically to this version.
- Generated context bundles currently report their source revision as UNKNOWN. Until a release binds bundles to their sources, they do not meet the revision-bound transport described in [OPERATING.md](OPERATING.md) and EVAL-D09 in [AGENT_EVALS.md](AGENT_EVALS.md) and must not be relied on as such.

## Inherited status (as recorded in bAIble v2, not re-verified here)

The table below is the status bAIble v2 recorded for the ecosystem layers (source: bAIble v2 `STATUS.md` at revision `80b7262`, no longer public). It is kept so the state stays visible; it has not been re-verified for this version, and runtime evidence behind it lives in private FederAItion.

| Area | Designed | Built | Tested | Verified | Integrated |
|---|---|---|---|---|---|
| Core governance | yes | yes | documentation audit | current repo inspected | yes |
| Human View (README) | yes | yes | navigation/self-audit | links inspected | yes |
| AI View (OPERATING) | yes | yes | activation/discovery eval scenarios defined | repo presence inspected; cross-agent behavior still under evaluation | yes |
| AI discovery/loading layer | yes | yes — discovery contract, adapters, graph routing, bundle tooling and CI | repository integrity CI passed; EXP-AI-DISCOVERY-001 defined | structurally verified; NOT YET cross-agent behavior verified | yes |
| Reality Check contract | yes | yes | anti-drift test defined | current public meaning inspected | yes |
| Fact Check contract | yes | yes | outcome model defined | current public meaning inspected | yes |
| Context Item / relations | yes | yes | private prototype tests exist | public contract + private evidence partially verified | yes |
| rAIda public contract | yes | private runtime built | dedicated private run passed | bounded runtime behavior verified for the exercised path; editorial work not covered | yes |
| Watchdog public contract | yes | private runtime built | live tests exist | bounded continuity behavior verified | yes |
| WheeAIls | yes | public relevance contract built | activation/relevance evals defined | concept + behavior contract; cross-agent verification pending | yes |
| Wolf | yes | public onboarding/activation contract built | clean-chat behavioral observation + evals defined | bounded observation only; systematic cross-agent verification pending | yes |
| RC / FC runtime alignment | yes | private runtime aligned | private runtime + smoke | bounded behavior verified | yes |
| UnAiversed private naming consolidation | concept defined | active + historical paths explicitly separated | private cleanup verified by repository inspection | canonical active path is unAIversed; unAiversed retained as history | yes |
| Local process contracts / rule stack | yes | private runtime built | multi-stage bounded + live tests | versioning/discovery/locked authority path verified | yes |
| Task/process graph | yes | private runtime built | live graph projection + continuation | graph-only active dispatch verified | yes |
| Failure / recovery | yes | private runtime built | live fail→retry→recovery chain | original failure preserved; recovered process verified | yes |
| Reconstructable handoff | yes | private runtime built | restart/reconstruction tests | graph/evidence/rule drift forces reconstruct | yes |
| Perspective divergence | yes | private runtime built + UnAiversed object model | runtime + UnAiversed tests | preserved/nonblocking vs blocking divergence verified | yes |
| Semantic reconstruction audit | yes | private runtime built | integration coverage audit | current source inventory covered with explicit open issues | yes |
| Real project pilot | bounded pilot defined | private viewer build executor | private run + smoke | real viewer branch build passed through graph/rAIda/evidence path | yes |

bAIble v2 described itself as a usable living baseline ("ecosystem baseline status: COMPLETE, 2026-09-27"), within the scope its private runtime evidence exercised. That claim belongs to bAIble v2.

## Origin

bAIble v2 was consolidated on 2026-10-20 from 50 documents to 20 active ones. Its history and old-to-new file map stay in bAIble v2 (revision `80b7262`, no longer public) and are not active guidance here.

## Open questions

These stay visible rather than being invented away:

- Does documented governance actually activate at the moment of transition in fresh agents, without the human naming it? (activation recall/precision and human compensation rate, [AGENT_EVALS.md](AGENT_EVALS.md) M03–M04; not yet measured systematically)
- Full production implementation of a canonical UnAiversed graph and viewer.
- How much relationship metadata should become machine-enforced schema versus documented contract.
- The exact interface for the Human and AI views.
- How reminders are selected automatically across different agent environments.
- How a generated single-file context bundle is distributed without becoming a second truth store.
- Which checks need independent evidence in each project domain.
- How living public releases are versioned without history taking over the main navigation.
- How a fresh agent can tell that what its tools returned is the current version. In evaluation runs an agent used a historical document as current guidance; the cause is not established.

## Self-audit before a release

Automated by `scripts/validate_discovery.py`: referenced files exist; graph resources, routing hints and llms.txt links resolve; graph predicates, node types and failure-mode coverage match [vocabulary.json](vocabulary.json); blocker lists use only canonical states; every active document is in the manifest; no case-only path collisions; no private run identifiers or listed private project names (the list is supplied from outside the repository; without it the name check is reported as not performed).

Checked by a person or reviewing agent:

- purpose and scope are clear; a beginner can start without private context;
- Human and AI views stay understandable; the full capability map stays discoverable while mechanisms are dormant;
- adapters point to canonical sources instead of becoming duplicate truth stores;
- principles are distinguishable from examples and culture;
- facts, observations, interpretations, hypotheses, decisions, evidence and unknowns stay distinguishable;
- Reality Check, Fact Check, Verification and Acceptance are not collapsed;
- human authority stays visible; rAIda, Watchdog, Wolf and WheeAIls do not acquire authority;
- evidence and verification are distinct from self-report; implementation claims have accessible evidence;
- contradictions show the actual claims and sources, not a yellow status;
- provenance is preserved; relations do not transfer truth, scope, authority or visibility;
- restricted-access agents have a bounded fallback without repeated manual navigation;
- generalized lessons do not expose private origins; sensitive identifiers and credentials are absent;
- optional architecture exists only where real need justifies it; history does not override current navigation;
- a concept has one home (candidate R-025); runtime or test success is not presented as editorial completeness.

A failed item triggers investigation. It is not by itself proof that the underlying idea is wrong.

## Provenance of this version

Every file of this version comes from bAIble v2 at revision `80b7262de738d5fdb6e07fe82f31aff6c77ce999`, at the same path. **P** = carried over with meaning unchanged; **P (identity)** = only the version name changed; **R** = reworked as described. History and other bAIble v2 material not listed here stays in bAIble v2 (revision `80b7262`, no longer public) and is not part of this version. Carrying a file over does not carry over evidence that it works.

After this version was published, bAIble v2 stopped being public (2026-10-31). Links to it were then replaced by plain-text references naming the same files and revision; meaning and provenance are unchanged.

| File | Kind | Change |
|---|---|---|
| `.github/workflows/discovery-contract.yml` | P | None |
| `AGENTS.md` | R | Title and repository name; history reminder points to bAIble v2 |
| `AGENT_EVALS.md` | R | Title; added candidate method notes EVAL-MC01…MC07 (not canonical) |
| `AI_CONTEXT_MANIFEST.json` | P | None |
| `BIBLE.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `BOUNDARY.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `CONTEXT.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `CONTINUITY.md` | R | Title |
| `ECOSYSTEM.md` | R | Title; chronology reference names bAIble v2 |
| `ECOSYSTEM_GRAPH.json` | R | No change (reviewed; all resources are current relative paths) |
| `FACT_CHECK.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `FAILURE_MODES.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `LEARNING.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `ONBOARDING.md` | R | Title; starter instruction names this version |
| `OPERATING.md` | R | Title; references to history and the discovery experiment name bAIble v2 |
| `RAIDA_WATCHDOG.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `README.md` | R | Entry adapted: title, draft-candidate status, previous-version reference |
| `REALITY_CHECK.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `SONG_TWO.md` | P | None |
| `STATUS.md` | R | Own status of this version; inherited bAIble v2 status kept as such; this provenance table |
| `VERIFICATION.md` | P (identity) | Title or name only: bAIble v2 → bAIble-rAIssonance |
| `WHEEAILS.md` | P | None |
| `WOLF.md` | P | None |
| `llms.txt` | R | Title, repository addresses; history reminder points to bAIble v2 |
| `scripts/build_ai_context.py` | R | Bundle title; planned repository; source revision reported as UNKNOWN |
| `scripts/validate_discovery.py` | R | Repository identity; stricter llms.txt link check (own repository, path stays inside the tree) |
| `vocabulary.json` | P (identity) | purpose text names this version; vocabularies unchanged |
