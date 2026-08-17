# CodexSaver v2 Restart Confirmation

Date: 2026-05-12

## Goal

Confirm that the benchmark report is produced by CodexSaver v2, not by an older
in-memory MCP server.

## Restart Steps

- Found old active MCP process: `python ./codexsaver_mcp.py`
- Stopped old process: `PID 62963`
- Confirmed no `codexsaver_mcp` process remained afterward
- Started the global launcher manually through stdio:
  `/Users/f/.codexsaver/codexsaver_mcp.py`

## V2 Evidence

- MCP initialize response: `serverInfo.name=codexsaver`
- MCP initialize response: `serverInfo.version=0.2.0`
- MCP tools/list includes: `delegate_task`
- MCP tools/list includes: `delegate_work_packet`
- `delegate_work_packet` schema describes: `bounded v2 coding work packet`
- MCP tools/call returned: `preflight_satisfied=true`
- MCP tools/call verification reason: `Work packet already satisfied before delegation.`

## Installed CLI Evidence

- Editable install succeeded: `codexsaver-0.2.0`
- CLI path: `/opt/anaconda3/bin/codexsaver`
- Imported package path: `/Users/f/GitHub/CodexSaver/codexsaver/__init__.py`
- Global launcher source root: `/Users/f/GitHub/CodexSaver`
- Provider: `deepseek`
- Provider model: `deepseek-chat`
- Provider key source: local persisted config

## 2026-05-12 Benchmark

Method: Codex-only is a normalized counterfactual baseline with cost index `1.00`.
CodexSaver results are real bounded work-packet runs through the installed v2 code.
`worker` means DeepSeek produced a patch that passed sandbox verification.
`preflight` means the allowlisted check passed before any worker model call.

| Task | Kind | Mode | Status | Codex-only cost | CodexSaver cost | Savings | Effect | Latency |
|---|---|---|---|---:|---:|---:|---:|---:|
| Create v2 smoke doc | docs | worker | success | 1.00 | 0.55 | 45% | 1.0 | 2.46s |
| Add generated cost test | tests | worker | success | 1.00 | 0.55 | 45% | 1.0 | 14.95s |
| Add package version metadata | small_code | preflight | success | 1.00 | 0.00 | 100% | 1.0 | 0.03s |
| Document work-packet CLI | docs | worker | success | 1.00 | 0.55 | 45% | 1.0 | 10.92s |
| Create Chinese v2 note | zh_docs | worker | success | 1.00 | 0.55 | 45% | 1.0 | 2.42s |

## Summary

- Success rate: `5/5`
- Worker delegation: `4/5`
- Preflight already-satisfied: `1/5`
- Average latency: `6.16s`
- Worker-only average latency: `7.69s`
- Average normalized CodexSaver cost index: `0.44`
- Average estimated savings: `56%`
- Worker-only estimated savings: `45%`

## Verification

- Full unit test suite after v2 fixes: `97 passed in 0.49s`
- Secret scan: no DeepSeek key or `sk-...` token found in git diff
- All benchmark patches were applied and checked in sandbox workspaces only

## Conclusion

This report is confirmed to be for CodexSaver v2. The proof is the restarted
global launcher returning `serverInfo.version=0.2.0`, exposing
`delegate_work_packet`, and returning the v2-only `preflight_satisfied=true`
field from an MCP tools/call.
