# CodexSaver Agent Policy

You have access to the MCP tool `codexsaver.delegate_task`.

Use CodexSaver when it can reduce cost safely.

## Good tasks to delegate

- repo scanning and code search
- code explanation and summarization
- writing unit tests
- fixing lint/type errors
- documentation updates
- boilerplate generation
- small, localized refactors
- read-only code review drafts
- localized bug fixes with explicit checks
- structured data transformations and localization
- repetitive mechanical changes across up to 40 files

## Do not delegate

- architecture decisions
- auth/security/payment logic
- database migrations
- permissions or access-control changes
- production deployment logic
- ambiguous requirements
- final review before applying changes

## Workflow

1. Decide whether the task is low/medium risk, bounded, and outside protected domains.
2. If bounded and verifiable, call `codexsaver.delegate_task` or `codexsaver.delegate_work_packet`.
3. Review the returned patch and risk notes.
4. Apply changes only if safe.
5. Run or recommend `commands_to_run`.
6. If CodexSaver returns `needs_codex`, take over directly.

## Principle

DeepSeek does the cheap work. Codex makes the decisions.
