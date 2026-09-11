# Workflow diagrams

- `workflow-overview-en.svg`: compact lifecycle and grade-dependent preparation.
- `workflow-detailed-en.svg`: ordered gates, evidence blockers, optional Blind Audit, and final authorization.

The SVG files are editable text sources and have no external fonts, images, scripts, or remote resources. Keep them readable as standalone assets; text remains selectable. PNG previews are optional viewing artifacts, not an additional source of policy.

Canonical meanings live in `../docs/workflow.md`, `../docs/risk-grades.md`, `../docs/review-gates.md`, and `../docs/verification.md`. When those meanings change, update both diagrams and their README descriptions together.

Check XML validity, local link targets, readable rendering, and these semantics: lean paths skip unnecessary design review; Large distinguishes AS-IS and PLAN; Blind Audit is optional; unmet required evidence/review blocks integration; final authorization is distinct from design approval. XML/render checks are not runtime or independent-review evidence.
