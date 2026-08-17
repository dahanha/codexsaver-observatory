from __future__ import annotations

from typing import List

from .schema import RouteDecision, RiskLevel, TaskType

PROTECTED_PATH_KEYWORDS = [
    "auth", "oauth", "jwt", "session", "security", "permission", "rbac",
    "payment", "payments", "billing", "invoice", "migration", "migrations",
    "schema", "infra", "terraform", ".github/workflows", ".env", "secret",
    "key", "token",
    "\u8ba4\u8bc1", "\u9274\u6743", "\u5b89\u5168", "\u6743\u9650", "\u652f\u4ed8", "\u8d26\u5355",
    "\u8fc1\u79fb", "\u6570\u636e\u5e93", "\u5bc6\u94a5", "\u4ee4\u724c", "\u751f\u4ea7", "\u90e8\u7f72",
]

HIGH_RISK_INSTRUCTION_KEYWORDS = [
    "authentication", "authorization", "permission", "security", "payment",
    "billing", "migration", "database schema", "encrypt", "decrypt", "secret",
    "token", "production", "deploy",
    "\u8ba4\u8bc1", "\u9274\u6743", "\u6388\u6743", "\u6743\u9650", "\u5b89\u5168", "\u652f\u4ed8",
    "\u8d26\u5355", "\u8ba1\u8d39", "\u8fc1\u79fb", "\u6570\u636e\u5e93\u8fc1\u79fb", "\u6570\u636e\u5e93\u67b6\u6784",
    "\u52a0\u5bc6", "\u89e3\u5bc6", "\u5bc6\u94a5", "\u4ee4\u724c", "\u751f\u4ea7", "\u90e8\u7f72", "\u4e0a\u7ebf",
]

REPETITIVE_TASK_KEYWORDS = [
    "repetitive", "mechanical", "batch", "bulk", "mass update", "replace all",
    "apply the same change", "normalize", "copy this pattern",
    "\u91cd\u590d", "\u53cd\u590d", "\u91cd\u590d\u6027", "\u91cd\u590d\u5de5\u4f5c", "\u673a\u68b0\u6027", "\u6279\u91cf",
    "\u6279\u91cf\u4fee\u6539", "\u6279\u91cf\u66ff\u6362", "\u6309\u76f8\u540c\u89c4\u5219", "\u7edf\u4e00\u4fee\u6539", "\u6279\u91cf\u5904\u7406",
]

DELEGATABLE: set[TaskType] = {
    "code_search", "explain", "write_tests", "fix_lint", "docs", "boilerplate",
    "simple_refactor", "local_fix", "data_transform", "review_draft",
}

MAX_AUTOMATIC_FILES = 40
MEDIUM_FILE_THRESHOLD = 12
PROTECTED_READONLY_TASKS: set[TaskType] = {
    "code_search", "explain", "write_tests", "docs", "review_draft",
}


class Router:
    def classify(self, instruction: str) -> TaskType:
        text = instruction.lower()
        if self._has(text, ["update", "write", "add", "更新", "编写", "补充", "添加"]) and self._has(
            text, ["readme", "documentation", "docstring", "文档", "说明", "注释"]
        ):
            return "docs"
        if self._has(text, [
            "update readme", "write documentation", "add docstrings",
            "更新文档", "更新说明", "编写文档", "补充文档", "添加注释",
        ]):
            return "docs"
        if self._has(text, [
            "find", "search", "locate", "where is", "scan", "grep",
            "\u67e5\u627e", "\u641c\u7d22", "\u67e5\u4e00\u4e0b", "\u5b9a\u4f4d", "\u54ea\u91cc", "\u626b\u63cf", "\u68c0\u7d22",
        ]):
            return "code_search"
        if self._has(text, [
            "explain", "summarize", "what does", "walk me through",
            "\u89e3\u91ca", "\u8bf4\u660e", "\u603b\u7ed3", "\u6982\u8ff0", "\u8bb2\u89e3",
            "\u600e\u4e48\u5de5\u4f5c", "\u5982\u4f55\u5de5\u4f5c", "\u5e2e\u6211\u7406\u89e3",
        ]):
            return "explain"
        if self._has(text, [
            "test", "unit test", "pytest", "jest", "spec", "coverage",
            "\u6d4b\u8bd5", "\u5355\u5143\u6d4b\u8bd5", "\u6d4b\u8bd5\u7528\u4f8b", "\u8986\u76d6\u7387",
        ]):
            return "write_tests"
        if self._has(text, [
            "lint", "eslint", "prettier", "mypy", "ruff", "type error", "tsc",
            "\u4ee3\u7801\u68c0\u67e5", "\u9759\u6001\u68c0\u67e5", "\u683c\u5f0f\u5316", "\u7c7b\u578b\u9519\u8bef", "\u7c7b\u578b\u68c0\u67e5",
        ]):
            return "fix_lint"
        if self._has(text, [
            "fix bug", "bugfix", "repair bug", "resolve issue", "patch bug",
            "\u4fee\u590d bug", "\u4fee\u590d\u95ee\u9898", "\u4fee\u590d\u9519\u8bef", "\u5c40\u90e8\u4fee\u590d", "\u6392\u67e5\u5e76\u4fee\u590d",
        ]):
            return "local_fix"
        if self._has(text, [
            "translate", "localize", "convert json", "convert csv", "transform data",
            "map fields", "extract fields", "\u7ffb\u8bd1", "\u672c\u5730\u5316", "\u8f6c\u6362 json", "\u8f6c\u6362 csv",
            "\u6570\u636e\u8f6c\u6362", "\u5b57\u6bb5\u6620\u5c04", "\u63d0\u53d6\u5b57\u6bb5",
        ]):
            return "data_transform"
        if self._has(text, [
            "readme", "docs", "documentation", "comment", "docstring",
            "\u6587\u6863", "\u8bf4\u660e\u6587\u6863", "\u6ce8\u91ca", "\u6587\u6863\u5b57\u7b26\u4e32",
        ]):
            return "docs"
        if self._has(text, [
            "boilerplate", "scaffold", "template", "generate",
            "\u811a\u624b\u67b6", "\u6837\u677f\u4ee3\u7801", "\u6a21\u677f", "\u751f\u6210\u57fa\u7840\u4ee3\u7801", "\u751f\u6210\u6837\u677f",
        ]):
            return "boilerplate"
        if self._has(text, [
            "refactor", "rename", "cleanup", "simplify", "deduplicate",
            "\u91cd\u6784", "\u91cd\u547d\u540d", "\u6e05\u7406", "\u7b80\u5316", "\u53bb\u91cd", "\u6574\u7406\u4ee3\u7801",
            *REPETITIVE_TASK_KEYWORDS,
        ]):
            return "simple_refactor"
        if self._has(text, [
            "review", "check this patch", "audit", "\u8bc4\u5ba1", "\u5ba1\u67e5", "\u68c0\u67e5\u8865\u4e01",
            "\u68c0\u67e5\u8fd9\u4e2a\u6539\u52a8", "\u4ee3\u7801\u5ba1\u67e5", "\u5ba1\u8ba1",
        ]):
            return "review_draft"
        return "unknown"

    def risk(self, instruction: str, files: List[str]) -> tuple[RiskLevel, List[str]]:
        text = instruction.lower()
        paths = "\n".join(files).lower()
        protected_hits = sorted({k for k in PROTECTED_PATH_KEYWORDS if k in paths or k in text})
        high_instruction_hits = sorted({k for k in HIGH_RISK_INSTRUCTION_KEYWORDS if k in text})
        if high_instruction_hits:
            return "high", high_instruction_hits
        if protected_hits:
            if self.classify(instruction) in PROTECTED_READONLY_TASKS:
                return "medium", protected_hits
            return "high", protected_hits
        if len(files) > MEDIUM_FILE_THRESHOLD:
            if self._has(text, REPETITIVE_TASK_KEYWORDS) and len(files) <= MAX_AUTOMATIC_FILES:
                return "low", []
            return "medium", []
        return "low", []

    def decide(self, instruction: str, files: List[str]) -> RouteDecision:
        task_type = self.classify(instruction)
        risk, protected_hits = self.risk(instruction, files)
        if len(files) > MAX_AUTOMATIC_FILES:
            return RouteDecision(route="codex", task_type=task_type, risk="medium",
                reason=f"Task exceeds the automatic delegation limit of {MAX_AUTOMATIC_FILES} files.",
                protected_hits=protected_hits)
        if risk == "high":
            return RouteDecision(route="codex", task_type=task_type, risk=risk,
                reason="High-risk task or protected domain detected.", protected_hits=protected_hits)
        if task_type == "unknown":
            return RouteDecision(route="codex", task_type=task_type, risk=risk,
                reason="Ambiguous task type.", protected_hits=protected_hits)
        if task_type not in DELEGATABLE:
            return RouteDecision(route="codex", task_type=task_type, risk=risk,
                reason=f"Task type '{task_type}' is not delegatable.", protected_hits=protected_hits)
        if risk == "medium" and protected_hits and task_type not in PROTECTED_READONLY_TASKS:
            return RouteDecision(route="codex", task_type=task_type, risk=risk,
                reason="Protected-domain modification requires Codex.", protected_hits=protected_hits)
        reason = "Task is low/acceptable risk."
        if self._has(instruction.lower(), REPETITIVE_TASK_KEYWORDS):
            reason = "Task is simple/repetitive, bounded, and low risk."
        elif risk == "medium":
            reason = "Task is medium risk but bounded, non-protected, and verifiable by Codex."
        return RouteDecision(route="deepseek", task_type=task_type, risk=risk,
            reason=reason, protected_hits=protected_hits)

    @staticmethod
    def _has(text: str, words: List[str]) -> bool:
        return any(w in text for w in words)
