<!-- CODEXSAVER:BEGIN -->
---
version: "1.0"
project_name: "New project"
codexsaver_profile: "basic"
---

# CodexSaver Workflow

## Tool Priority

- Delegate simple, repetitive, mechanical, low-risk work to DeepSeek first when the scope is clear and the result is easy to verify.
- If Codex judges a task to be low-risk, bounded, and mechanically verifiable, it may delegate it even when the wording does not exactly match the examples below.
- For a safe task that does not match a fixed keyword, call `codexsaver.delegate_task` with `codex_approved=true`, explicit files, and acceptance constraints. Never use this override for protected or high-risk work.
- Prefer `codexsaver.orchestrate_task` for decomposable low-risk work spanning docs, tests, explanation, or bounded implementation.
- For database/schema/import tasks, use CodexSaver only for safe preparation: readonly inspection, script drafts, validation SQL, dry-run plans, and reports.
- Prefer `codexsaver.run_specialist` for an explicit specialist task such as explanation or tests only.
- Prefer `codexsaver.delegate_work_packet` for a single bounded patch with explicit allowed files and checks.
- Fall back to direct Codex execution only when CodexSaver returns `needs_codex`, fails repeatedly, or the task touches a protected domain.

## Low-Risk Tasks That Should Usually Use CodexSaver

- unit tests
- repeated test generation or repetitive updates across a bounded file set
- docstrings, JSDoc, README updates
- code explanation and repository scanning
- formatting and boilerplate
- read-only code review drafts and patch analysis
- localized bug fixes with explicit reproduction or acceptance checks
- structured data conversion, field mapping, translation, and localization
- simple repetitive edits, bulk replacements, renames, normalization, and other mechanical changes with explicit file scope
- small bounded refactors with explicit file scope and no architectural decision
- database read-only inspection and dry-run validation planning

## DeepSeek Delegation Gate

Use DeepSeek only when all of these are true:

- the task is low/medium risk and does not modify protected domains;
- the work is repetitive, read-only, locally fixable, data-oriented, or bounded by explicit files and checks;
- the allowed files and acceptance checks are clear;
- Codex can review the result and keep final judgment.

Normal bounded tasks may include up to twenty context files. Explicitly repetitive work may include up to forty files. Bounded work packets may use up to four repair iterations and 600 changed lines by default. Larger or ambiguous changes stay in Codex unless split into smaller packets.

## Do Not Route To CodexSaver By Default

- auth, security, payment, permissions, secrets
- destructive migrations or deploy logic
- direct database writes, schema migrations, destructive cleanup, or operations requiring credentials
- ambiguous architecture decisions
- final merge judgment without Codex review

## Verification Expectations

- When CodexSaver returns checks, review them before applying changes.
- Prefer allowlisted test or lint commands for generated tests and docs updates.
- If CodexSaver reports overlapping patch outputs or protected-path conflicts, keep the task in Codex.
- If CodexSaver returns a `handoff`, reuse its delegated evidence and keep listed `blocked_actions` in Codex.
<!-- CODEXSAVER:END -->
