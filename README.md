# CodexSaver Observatory

CodexSaver Observatory 是一个完整的 Codex + DeepSeek 任务路由项目，仓库同时包含：

- `codexsaver-engine/`：CodexSaver Python 引擎与 MCP 服务；
- `index.html` / `server.py`：本地可视化仪表盘；
- 中文任务分类、简单重复任务委派、Codex 主动批准委派；
- DeepSeek 启用/停用、API Key 配置和连接测试；
- 脱敏路由事件记录与调用理由展示。

## Windows 安装

要求 Python 3.10 或更高版本。

```powershell
git clone https://github.com/dahanha/codexsaver-observatory.git
cd codexsaver-observatory
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

安装脚本会：

1. 以 editable 模式安装仓库内的 `codexsaver-engine`；
2. 在 `%USERPROFILE%\.codex\config.toml` 注册全局 `codexsaver` MCP；
3. 写入稳定的 MCP 启动器并运行安装检查。

安装完成后重启 Codex。新的 Codex 会话中应能看到 `codexsaver.*` 工具。

## 启动仪表盘

```powershell
.\start.ps1
```

也可以手动启动：

```powershell
py -3 server.py
```

打开 `http://127.0.0.1:8765`。在 **DeepSeek 设置** 中填写 API Key、开启自动委派并点击 **测试连接**。

## 路由规则

DeepSeek 适合处理范围明确、可验证、低风险的工作，例如：

- 搜索、扫描、解释和总结；
- 单元测试、文档、格式化和样板代码；
- 最多 20 个文件的简单重复或批量修改；
- Codex 明确判断可以委派的低/中风险任务。

认证、安全、支付、权限、数据库迁移、生产部署、模糊架构决策和其他高风险工作保留给 Codex。每次调用 DeepSeek 都会记录并展示调用原因，Codex 保留最终审核权。

## 本地数据

配置文件：

```text
%USERPROFILE%\.codexsaver\config.json
```

路由事件：

```text
%USERPROFILE%\.codexsaver\events.jsonl
```

API Key、文件内容和完整任务指令不会写入 Git 或路由事件。API Key 只会在测试连接或真实委派时发送到配置的 DeepSeek API 地址。

## 验证安装

```powershell
codexsaver doctor --workspace .
codexsaver "为工具函数添加单元测试" --dry-run
```

如果当前终端还找不到 `codexsaver` 命令，可以直接运行：

```powershell
py -3 .\codexsaver-engine\cli.py doctor --workspace .
```

## 来源

内置引擎基于 [fendouai/CodexSaver](https://github.com/fendouai/CodexSaver) `0.3.6`，本仓库增加了中文分类、重复任务规则、DeepSeek 开关、明确调用理由和 Observatory 事件记录。
