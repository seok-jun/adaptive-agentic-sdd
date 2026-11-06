# Selected-task guard

Read this only after selecting this starter W. These protections are retained by the starter for that task; they add restrictions, never permissions. P's existing common rules and authority apply whether or not W is selected. Teams may separately adopt common protections into P through their own decision process. This file does not create a product AGENTS block.

- Preserve unrelated user changes: do not reset, checkout, clean or revert them.
- Keep secrets, credentials and protected personal information out of development artifacts. Follow P's evidence/disclosure rules. Do not copy conversation logs; retain only permitted requirements and settled decisions needed for the task.
- Check file, module, API and setting names against actual sources; do not invent them.
- Keep changes within the task's authorized scope. Do not add unrelated refactors, renames, formatting, dependencies or features. Apply allowed/forbidden edit boundaries; forbidden paths take precedence.
- Respect P's module and integration boundaries. Under this starter's lane procedure, stop overlapping implementation paths or integration-only edits until coordination is resolved.
- Do not call unrun tests/builds/lints/device checks PASS. Required failures, unknown results and BLOCKED checks remain visible; they do not become complete through a summary.
- Use the current execution shell first. Use a bounded cross-shell fallback only when the current-shell or portable method is unavailable.
- Read repository text as UTF-8 first unless there is evidence of another encoding. Do not infer a procedure from garbled output.
- Keep the selected W snapshot stable during the product task. Customize W through a separate project-owned change, then explicitly select the new commit; upstream approval is not required. In the external adoption path, application documents are editable sources rather than legacy generated files.
- Do not invent human decisions, reduce approval conditions or create, broaden or confirm delegations. Follow P's actual authority sources. Additional method-specific judgment points do not replace those sources.
- Stop only work dependent on an unresolved human decision; independent work may continue. If the environment cannot ask, keep the dependent work stopped and record the unresolved question at the declared location.

These are the default restrictions of the selected starter. Project owners can evolve W; that does not grant an agent authority to waive product requirements, budget, host restrictions or a user's decisions. Follow the selected entry's locally adopted support documents only within that method's scope.

## Temporary outputs are part of the write boundary

Allowed/forbidden paths cover not only product files but also helper scripts, message files, copies, logs, caches and build outputs that the agent creates or directs commands to create. Prefer existing tools, stdin or memory before creating another tool/file. When disk is needed, use an already authorized task-specific scratch/output path. The OS temp directory, home and other projects are not authorized defaults. Check the resolved path including symlinks/junctions; scratch permission does not expand product edit permission. If a needed path is undeclared, stop only the dependent write. Direct TMPDIR/TMP/TEMP and language-specific cache/output settings to the same authorized area. Do not arbitrarily copy or clean host-managed session records.

When enforcement is required, configure the existing host sandbox/tool writable roots and verify them with harmless allowed/denied probes before task work. Do not bypass a denied write with another shell or path. A declaration, environment variable or READY result does not prove isolation. If sandbox enforcement is absent or untested, record it as unconfirmed.
