# CodexSaver Observatory

Local dashboard for seeing when Codex routes work to DeepSeek, why the route was chosen, and whether the worker result passed verification.

## Start

```powershell
py -3 server.py
```

Open `http://127.0.0.1:8765`.

## DeepSeek settings

The **DeepSeek 设置** panel can:

- save or replace the local DeepSeek API Key;
- enable or disable automatic DeepSeek delegation;
- make a small live request to test the API connection.

Settings are saved only to `%USERPROFILE%\.codexsaver\config.json`. The API Key is never stored in browser storage, dashboard events, or this Git repository. When DeepSeek is disabled, eligible tasks are returned to Codex without an external model call.

The server reads routing events from:

```text
%USERPROFILE%\.codexsaver\events.jsonl
```

Override the location when needed:

```powershell
$env:CODEXSAVER_EVENTS_FILE = "C:\path\to\events.jsonl"
py -3 server.py
```

The dashboard starts with a small built-in sample so the layout is useful before the first live event. It also supports importing JSON or JSONL files from the browser.

## CodexSaver integration

The installed CodexSaver engine writes one redacted event per routing result. It records route, provider, task type, risk, status, reason, verification detail, and estimated savings. It never records API keys, file contents, or the full instruction.

The reference helper is in [`integrations/codexsaver_observability.py`](integrations/codexsaver_observability.py). The active editable CodexSaver install uses the same helper at `codexsaver/observability.py`.

If CodexSaver is upgraded or reinstalled, reapply that small observability integration before expecting new live events.

## Data model

Each JSONL line looks like this:

```json
{"event_id":"...","timestamp":"2026-08-17T10:20:00+08:00","route":"deepseek","provider":"deepseek","task_type":"write_tests","risk":"low","status":"success","reason":"...","detail":"...","estimated_savings_percent":45}
```

## Safety

This project is local-only by default. The dashboard reads the local CodexSaver settings only to display masked status and perform settings actions initiated in the UI. The API Key is sent only to the configured DeepSeek endpoint when **测试连接** is clicked or when CodexSaver delegates a task. Review event contents before importing or publishing them.

## Another computer

Clone this repository, install CodexSaver on that computer, start `server.py`, and enter that computer's DeepSeek API Key in the dashboard. Keys are intentionally not transferred through GitHub.
