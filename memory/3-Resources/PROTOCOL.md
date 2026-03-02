# OpenClaw 协同公共协议 (Shared Protocol V2.1)

> 双核共用法典 | 解决 V2.0 规则重复和漂移隐患

---

## 1. 统一身份与红线

- **人类老板**：唯一称呼为 **Robin** (严禁使用 Robbie / Robin Zhang)
- **安全红线**：绝对禁止将 `jarvis-zorro-collab` (私有核心库) 的代码、密钥、策略暴露或推送到 `polymarket-reporter` (公有内容库)

---

## 2. 状态机与标签 (GitHub Labels)

| 标签 | 含义 | 触发者 |
| :--- | :--- | :--- |
| `@Zorro-Exec` | Jarvis 派发重度任务的唯一标识 | Jarvis |
| `In-Progress` | Zorro 认领并正在执行 | Zorro |
| `BLOCKED` | 触发 3 次错误熔断，Zorro 停止动作，等待 Jarvis 介入 | Zorro |
| `Needs-Review` | Zorro 本地 Schema 校验通过并提交 PR，等待验收 | Zorro |

---

## 3. 双轨路由表 (Routing Table)

| 业务场景 | 目标仓库 (`--repo`) | 谁执行 | 交付标准 |
| :--- | :--- | :--- | :--- |
| 信息抓取/洗数据 | `RobinZorro86/polymarket-reporter` | Zorro | 符合 Schema 的 JSON |
| 撰写日报/网站发布 | `RobinZorro86/polymarket-reporter` | Jarvis | Markdown 直接 Push |
| Aegis 系统/复杂工具 | `RobinZorro86/jarvis-zorro-collab` | Zorro | 提 PR + 测试用例 |
| 架构设计/代码审查 | `RobinZorro86/jarvis-zorro-collab` | Jarvis | Issue 拆解 + PR 审查 |

---

## 4. 版本历史

| 版本 | 日期 | 变更 |
| :--- | :--- | :--- |
| V2.1 | 2026-03-02 | 初始化全局公共协议 (Shared Protocol) |

---

*此文件由 Jarvis 初始化，双核共享阅读。修改需双方确认。*