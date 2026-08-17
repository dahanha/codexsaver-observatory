from __future__ import annotations

import pytest
from codexsaver.router import Router, DELEGATABLE, PROTECTED_PATH_KEYWORDS


class TestRouter:
    def setup_method(self):
        self.router = Router()

    def test_classify_code_search(self):
        assert self.router.classify("find all files with auth") == "code_search"
        assert self.router.classify("search for login function") == "code_search"
        assert self.router.classify("where is the user model") == "code_search"

    def test_classify_explain(self):
        assert self.router.classify("explain this code") == "explain"
        assert self.router.classify("what does this function do") == "explain"
        assert self.router.classify("summarize the repository") == "explain"

    def test_classify_write_tests(self):
        assert self.router.classify("add unit tests") == "write_tests"
        assert self.router.classify("write tests for auth service") == "write_tests"
        assert self.router.classify("generate pytest coverage") == "write_tests"

    def test_classify_fix_lint(self):
        assert self.router.classify("fix lint errors") == "fix_lint"
        assert self.router.classify("eslint fix") == "fix_lint"
        assert self.router.classify("mypy type check") == "fix_lint"

    def test_classify_expanded_tasks(self):
        assert self.router.classify("fix bug in the local cache helper") == "local_fix"
        assert self.router.classify("transform data and map fields") == "data_transform"
        assert self.router.classify("review this patch") == "review_draft"

    def test_classify_docs(self):
        assert self.router.classify("update readme") == "docs"
        assert self.router.classify("write documentation") == "docs"
        assert self.router.classify("add docstrings") == "docs"

    def test_classify_boilerplate(self):
        assert self.router.classify("generate boilerplate") == "boilerplate"
        assert self.router.classify("scaffold a new component") == "boilerplate"

    def test_classify_simple_refactor(self):
        assert self.router.classify("rename this variable") == "simple_refactor"
        assert self.router.classify("cleanup the code") == "simple_refactor"
        assert self.router.classify("批量修改这些重复文件") == "simple_refactor"

    def test_classify_chinese_tasks(self):
        assert self.router.classify("帮我搜索所有配置文件") == "code_search"
        assert self.router.classify("解释这个函数如何工作") == "explain"
        assert self.router.classify("为工具函数添加单元测试") == "write_tests"
        assert self.router.classify("更新项目说明文档") == "docs"

    def test_classify_unknown(self):
        assert self.router.classify("make it faster") == "unknown"
        assert self.router.classify("handle edge cases") == "unknown"

    def test_risk_low(self):
        risk, _ = self.router.risk("add unit tests for utils", ["src/utils/helper.py"])
        assert risk == "low"

    def test_risk_high_instruction(self):
        risk, hits = self.router.risk("encrypt user passwords", ["src/user/service.py"])
        assert risk == "high"
        assert "encrypt" in hits

    def test_risk_high_path(self):
        risk, hits = self.router.risk("refactor auth service", ["src/auth/login.go"])
        assert risk == "high"
        assert "auth" in hits

    def test_risk_medium_protected_with_readonly_task(self):
        risk, hits = self.router.risk("explain auth code", ["src/auth/service.py"])
        assert risk == "medium"
        assert "auth" in hits

    def test_risk_medium_file_count(self):
        files = [f"src/file_{index}.py" for index in range(13)]
        risk, _ = self.router.risk("add unit tests", files)
        assert risk == "medium"

    def test_decide_delegate_low_risk(self):
        result = self.router.decide("add unit tests for utils", ["src/utils/helper.py"])
        assert result.route == "deepseek"
        assert result.task_type == "write_tests"
        assert result.risk == "low"

    def test_decide_keep_high_risk(self):
        result = self.router.decide("fix security vulnerability", ["src/auth/login.go"])
        assert result.route == "codex"
        assert result.risk == "high"

    def test_decide_keep_architecture(self):
        result = self.router.decide("design new auth architecture", [])
        assert result.route == "codex"

    def test_decide_keep_unknown_task(self):
        result = self.router.decide("make the app better", ["src/app.py"])
        assert result.route == "codex"
        assert result.task_type == "unknown"

    def test_decide_delegate_code_search(self):
        result = self.router.decide("find all TODO comments", ["src/"])
        assert result.route == "deepseek"
        assert result.task_type == "code_search"

    def test_decide_delegate_simple_refactor(self):
        result = self.router.decide("refactor user service", ["src/user/service.py"])
        assert result.route == "deepseek"

    def test_decide_delegate_repetitive_batch_up_to_forty_files(self):
        files = [f"src/file_{index}.py" for index in range(40)]
        result = self.router.decide("按相同规则批量修改这些重复文件", files)
        assert result.route == "deepseek"
        assert result.risk == "low"
        assert "repetitive" in result.reason

    def test_decide_delegate_medium_non_protected_fix(self):
        files = [f"src/cache_{index}.py" for index in range(20)]
        result = self.router.decide("fix bug in the local cache helper", files)
        assert result.route == "deepseek"
        assert result.risk == "medium"

    def test_decide_blocks_more_than_forty_files(self):
        files = [f"src/file_{index}.py" for index in range(41)]
        result = self.router.decide("batch normalize these files", files)
        assert result.route == "codex"
        assert "40 files" in result.reason

    def test_decide_delegate_medium_readonly(self):
        result = self.router.decide("explain user service", ["src/user/service.py"])
        assert result.route == "deepseek"

    def test_protected_path_keywords_exist(self):
        assert "auth" in PROTECTED_PATH_KEYWORDS
        assert "security" in PROTECTED_PATH_KEYWORDS
        assert "payment" in PROTECTED_PATH_KEYWORDS
        assert "migration" in PROTECTED_PATH_KEYWORDS

    def test_delegatable_task_types(self):
        assert "code_search" in DELEGATABLE
        assert "write_tests" in DELEGATABLE
        assert "fix_lint" in DELEGATABLE
        assert "docs" in DELEGATABLE
        assert "boilerplate" in DELEGATABLE
        assert "simple_refactor" in DELEGATABLE
        assert "local_fix" in DELEGATABLE
        assert "data_transform" in DELEGATABLE
        assert "review_draft" in DELEGATABLE
