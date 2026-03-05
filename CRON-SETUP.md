# Cron 任务配置指南

> 网站 3.0 定期任务配置文档 - TASK-R3-003

## 概述

本文档说明如何配置和管理 Website 3.0 的定期自动化任务。

## 任务时间表

| 时间 | 任务 | 类型 |
|------|------|------|
| 00:00 JST | 每日市场数据抓取 | 每日 |
| 06:00 JST | 网站数据索引更新 | 每日 |
| 12:00 JST | 日报格式化发布 | 每日 |
| 18:00 JST | Git 备份与推送 | 每日 |
| 周一 09:00 JST | 周报生成 | 每周 |
| 周三 10:00 JST | 知识库内容更新 | 每周 |
| 周五 14:00 JST | Skills 性能评测 | 每周 |
| 周日 20:00 JST | 网站完整性检查 | 每周 |
| 每月 1 日 00:00 JST | 月度总结报告 | 每月 |
| 每月 15 日 10:00 JST | 全站内容审计 | 每月 |

## 配置方法

### 方法 1：使用 OpenClaw CLI

```bash
# 添加每日任务
openclaw cron add "0 0 * * *" "python3 /path/to/scrape_markets.py" --name "daily-market-scrape"

# 添加每周任务
openclaw cron add "0 9 * * 1" "python3 /path/to/generate_weekly_report.py" --name "weekly-report"

# 列出所有任务
openclaw cron list

# 删除任务
openclaw cron delete <task-id>
```

### 方法 2：使用配置文件

完整配置请参考 `website-cron-config.json`。

```bash
# 导入配置
openclaw cron import website-cron-config.json
```

## 通知配置

| 状态 | 动作 |
|------|------|
| 成功 | 静默 |
| 失败 | Telegram 通知 Robin |
| BLOCKED | 立即通知 Jarvis |

## 手动执行

```bash
# 手动运行市场抓取
python3 scripts/scrape_markets.py

# 手动运行索引更新
python3 scripts/update_index.py

# 手动运行健康检查
python3 scripts/site_health_check.py
```

## 监控

```bash
# 查看任务日志
openclaw cron logs <task-id>

# 查看任务状态
openclaw cron status
```

## 故障排除

### 任务未执行

1. 检查任务是否存在：`openclaw cron list`
2. 检查时间是否正确：`date`
3. 检查日志：`openclaw cron logs <task-id>`

### 任务失败

1. 查看错误日志
2. 手动运行命令检查输出
3. 检查依赖是否安装

### 通知未发送

1. 检查 Telegram 配置
2. 验证 chat_id 正确

## 相关文件

- 配置文件：`website-cron-config.json`
- 脚本目录：`scripts/`
- 报告目录：`reports/`

---

*最后更新：2026-03-05*