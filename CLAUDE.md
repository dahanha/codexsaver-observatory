# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

桌面番茄钟计时器 — 单页 HTML 应用，由轻量 Node.js HTTP 服务器托管。

## 常用命令

```
npm start        # 启动服务器 (localhost:3000)，自动打开浏览器
```

## 架构

- **server.js** — Node HTTP 服务器，端口 3000。所有请求均返回 `app.html`（路由仅有 `/` 和 `/app.html`）。启动后自动打开浏览器。
- **app.html** — 完整前端应用，纯原生 JS + CSS，不依赖任何框架。包含三种计时模式、SVG 环形进度条、浏览器通知和声音提醒。

### 计时器模式

- 专注 (focus): 25 分钟
- 短休 (shortBreak): 5 分钟
- 长休 (longBreak): 15 分钟

每完成 4 个专注周期自动触发一次长休。
