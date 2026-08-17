from __future__ import annotations

import argparse
import importlib.util
import json
import os
import stat
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
DEFAULT_EVENTS = Path.home() / ".codexsaver" / "events.jsonl"
DEFAULT_CONFIG = Path.home() / ".codexsaver" / "config.json"
DEFAULT_DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


def events_path() -> Path:
    configured = os.environ.get("CODEXSAVER_EVENTS_FILE", "").strip()
    return Path(configured).expanduser() if configured else DEFAULT_EVENTS


def config_path() -> Path:
    configured = os.environ.get("CODEXSAVER_CONFIG_FILE", "").strip()
    return Path(configured).expanduser() if configured else DEFAULT_CONFIG


def load_settings_config() -> dict:
    path = config_path()
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def mask_secret(value: str | None) -> str | None:
    if not value:
        return None
    return value if len(value) <= 8 else f"{value[:4]}...{value[-4:]}"


def current_settings() -> dict:
    config = load_settings_config()
    provider = config.get("providers", {}).get("deepseek", {})
    if not isinstance(provider, dict):
        provider = {}
    key = provider.get("api_key") or config.get("deepseek_api_key")
    codex_config = Path.home() / ".codex" / "config.toml"
    codex_config_text = codex_config.read_text(encoding="utf-8", errors="replace") if codex_config.exists() else ""
    return {
        "deepseek_enabled": bool(config.get("deepseek_enabled", True)),
        "api_key_configured": bool(key),
        "api_key_preview": mask_secret(key),
        "model": provider.get("model") or "deepseek-chat",
        "base_url": provider.get("base_url") or DEFAULT_DEEPSEEK_URL,
        "config_path": str(config_path()),
        "engine_installed": importlib.util.find_spec("codexsaver") is not None,
        "mcp_configured": "[mcp_servers.codexsaver]" in codex_config_text,
    }


def update_settings(payload: dict) -> dict:
    config = load_settings_config()
    if "deepseek_enabled" in payload:
        if not isinstance(payload["deepseek_enabled"], bool):
            raise ValueError("deepseek_enabled must be a boolean")
        config["deepseek_enabled"] = payload["deepseek_enabled"]
    api_key = payload.get("api_key")
    if isinstance(api_key, str) and api_key.strip():
        key = api_key.strip()
        config.setdefault("providers", {}).setdefault("deepseek", {})["api_key"] = key
        # Keep the legacy field in sync for older CodexSaver builds.
        config["deepseek_api_key"] = key
        config["provider"] = "deepseek"
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return current_settings()


def test_deepseek_connection() -> tuple[bool, dict]:
    config = load_settings_config()
    provider = config.get("providers", {}).get("deepseek", {})
    provider = provider if isinstance(provider, dict) else {}
    key = provider.get("api_key") or config.get("deepseek_api_key")
    if not key:
        return False, {"message": "尚未配置 DeepSeek API Key。"}
    url = provider.get("base_url") or DEFAULT_DEEPSEEK_URL
    model = provider.get("model") or "deepseek-chat"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with OK only."}],
        "max_tokens": 1,
        "stream": False,
    }).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response.read()
        return True, {"message": "DeepSeek API 连接成功。", "model": model}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:240]
        return False, {"message": f"DeepSeek 返回 HTTP {exc.code}。", "detail": detail}
    except urllib.error.URLError as exc:
        return False, {"message": "无法连接 DeepSeek。", "detail": str(exc.reason)}
    except TimeoutError:
        return False, {"message": "DeepSeek 连接超时。"}


def read_events() -> list[dict]:
    path = events_path()
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows[-500:]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/events":
            payload = {"events": read_events(), "source": str(events_path())}
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/settings":
            self._json_response(current_settings())
            return
        if parsed.path == "/api/health":
            payload = {"ok": True, "events_file": str(events_path()), "event_count": len(read_events())}
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path not in {"/api/settings/deepseek", "/api/settings/test"}:
            self.send_error(404)
            return
        if parsed.path == "/api/settings/test":
            ok, payload = test_deepseek_connection()
            self._json_response({"ok": ok, **payload}, status=200 if ok else 400)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            if not isinstance(payload, dict):
                raise ValueError("JSON body must be an object")
            self._json_response(update_settings(payload))
        except (ValueError, json.JSONDecodeError) as exc:
            self._json_response({"error": str(exc)}, status=400)

    def _json_response(self, payload: dict, status: int = 200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[dashboard] {self.address_string()} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the CodexSaver Observatory dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"CodexSaver Observatory: http://{args.host}:{args.port}")
    print(f"Watching: {events_path()}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
