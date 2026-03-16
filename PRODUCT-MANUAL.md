# pred101.com 产品手册

**版本**: 1.0  
**最后更新**: 2026-03-16 23:21 JST  
**维护人**: Zorro (main) / Zorro-Ops

---

## 一、产品概述

### 1.1 产品定位

**pred101 / Prediction Market 101** 是一个预测市场教育与信息平台，帮助用户：
- 学习预测市场基础知识
- 了解 Polymarket 等平台的使用方法
- 获取市场数据分析与洞察
- 掌握交易策略与风险管理

### 1.2 目标用户

| 用户类型 | 需求 | 对应内容 |
|----------|------|----------|
| **新手** | 了解预测市场是什么 | Learn 入门教程、FAQ |
| **进阶用户** | 学习交易策略 | Strategies、KOL 分析 |
| **专业用户** | 获取市场数据与洞察 | Reports、Simmer 扫描 |
| **开发者** | 集成 API 与工具 | Resources、APIs 文档 |

### 1.3 核心价值

- **双语支持**: 完整的中英双语内容（108 页）
- **结构化学习**: 从入门到进阶的完整路径
- **实时数据**: 每日/每周市场报告自动更新
- **策略库**: 经过验证的交易策略与方法论

---

## 二、网站架构

### 2.1 站点地图

```
www.pred101.com/
│
├── /en/                          # 英文站点 (47 页)
│   ├── index.html                # 英文首页
│   ├── about.html                # 关于我们
│   ├── knowledge-base/           # 知识库
│   │   ├── index.html
│   │   ├── strategies/           # 策略库
│   │   ├── kol/                  # KOL 分析
│   │   ├── resources/            # 资源
│   │   │   ├── index.html
│   │   │   ├── glossary/         # 术语表
│   │   │   ├── risk-management/  # 风险管理
│   │   │   └── apis/             # API 文档
│   │   └── tutorials/            # 教程
│   ├── reports/                  # 报告
│   │   ├── index.html
│   │   ├── daily/                # 日报
│   │   ├── weekly/               # 周报
│   │   └── simmer/               # Simmer 扫描
│   ├── learn/                    # 学习
│   │   ├── index.html
│   │   ├── basics/               # 基础
│   │   └── advanced/             # 进阶
│   ├── strategies/               # 策略（独立入口）
│   │   ├── copytrading.html      # 跟单交易
│   │   └── weather-trader.html   # 天气交易
│   ├── kol/                      # KOL（独立入口）
│   └── resources/                # 资源（独立入口）
│
├── /zh/                          # 中文站点 (61 页)
│   ├── index.html                # 中文首页
│   ├── about.html                # 关于我们
│   ├── knowledge-base/           # 知识库
│   │   ├── index.html
│   │   ├── strategies/
│   │   ├── kol/
│   │   ├── resources/
│   │   │   ├── index.html
│   │   │   ├── glossary/
│   │   │   ├── risk-management/
│   │   │   └── apis/
│   │   └── tutorials/
│   ├── reports/
│   │   ├── index.html
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── simmer/
│   ├── learn/
│   │   ├── index.html
│   │   ├── basics/
│   │   └── advanced/
│   ├── strategies/
│   │   ├── copytrading.html
│   │   └── weather-trader.html
│   ├── kol/
│   └── resources/
│
├── css/                          # 样式文件
├── js/                           # 脚本文件
├── assets/                       # 图片与媒体资源
├── data/                         # 数据文件
├── scripts/                      # 构建与自动化脚本
├── templates/                    # HTML 模板
├── sitemap.xml                   # 站点地图
├── robots.txt                    # 爬虫规则
└── vercel.json                   # Vercel 配置
```

### 2.2 页面统计

| 语言 | 内容页 | 入口页 | 总计 |
|------|--------|--------|------|
| English | 45 | 2 | 47 |
| 中文 | 59 | 2 | 61 |
| **总计** | **104** | **4** | **108** |

### 2.3 路由规则

**旧路径 → 新路径** (vercel.json 301 重定向):

| 旧路径 | 新路径 | 状态 |
|--------|--------|------|
| `/knowledge-base/*` | `/en/knowledge-base/*` | ✅ |
| `/reports/*` | `/en/reports/*` | ✅ |
| `/learn/*` | `/en/learn/*` | ✅ |
| `/strategies/*` | `/en/strategies/*` | ✅ |
| `/kol/*` | `/en/kol/*` | ✅ |
| `/resources/*` | `/en/resources/*` | ✅ |
| `/` (默认) | 根据浏览器语言选择 EN/ZH | ✅ |

---

## 三、设计系统

### 3.1 双层视觉架构

```
┌─────────────────────────────────────┐
│   概览层 (Overview Layer)            │
│   背景：深色 (#0a0a0a)              │
│   用途：导航、Hero、概览卡片         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   内容层 (Content Layer)             │
│   背景：浅色 (#ffffff / #f8f9fa)    │
│   用途：正文、表格、详细说明         │
└─────────────────────────────────────┘
```

### 3.2 颜色系统

#### 主色调
```css
--primary-dark: #0a0a0a;      /* 深色背景 */
--primary-light: #ffffff;     /* 浅色背景 */
--accent: #3b82f6;            /* 强调色（蓝色） */
--accent-hover: #2563eb;      /* 悬停色 */
```

#### 功能色
```css
--success: #22c55e;           /* 成功/上涨 */
--warning: #f59e0b;           /* 警告 */
--error: #ef4444;             /* 错误/下跌 */
--info: #3b82f6;              /* 信息 */
```

#### 文字色
```css
--text-primary: #0a0a0a;      /* 主文字（浅色背景上） */
--text-secondary: #6b7280;    /* 次要文字 */
--text-inverse: #ffffff;      /* 反色文字（深色背景上） */
```

### 3.3 字体系统

```css
/* 字体族 */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Fira Code', 'Consolas', monospace;

/* 字号 */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;

/* 行高 */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.6;
```

### 3.4 间距系统

```css
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-6: 24px;
--spacing-8: 32px;
--spacing-12: 48px;
--spacing-16: 64px;
```

### 3.5 组件规范

#### 导航栏
- 高度：`64px`
- 背景：深色层 `#0a0a0a`
- 文字：白色 `#ffffff`
- 链接悬停：透明度 `0.8`
- 包含：Logo、主导航、语言切换器

#### 按钮
```css
.btn-primary {
  background: var(--accent);
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 500;
}

.btn-primary:hover {
  background: var(--accent-hover);
}
```

#### 卡片
```css
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 24px;
}
```

---

## 四、内容规范

### 4.1 语言风格

#### 英文内容
- 语气：专业、清晰、友好
- 时态：一般现在时为主
- 人称：第二人称 "you"（拉近与读者距离）
- 日期格式：`Mar 16, 2026`
- 数字格式：`1,234.56`

#### 中文内容
- 语气：专业、清晰、亲切
- 时态：无严格时态，依上下文
- 人称：第二人称 "你" 或 "您"
- 日期格式：`2026 年 3 月 16 日`
- 数字格式：`1,234.56`

### 4.2 内容模板

#### 策略页面模板
```html
1. Hero 区域（策略名称 + 一句话概述）
2. 策略原理（为什么有效）
3. 操作步骤（如何做）
4. 风险提示（注意事项）
5. 案例演示（实际例子）
6. 相关资源（延伸阅读）
```

#### 报告页面模板
```html
1. 报告头（日期 + 类型 + 摘要）
2. 市场概览（整体情况）
3. 重点市场（详细分析）
4. 机会洞察（可操作建议）
5. 风险提示（风险因素）
6. 数据来源（透明度）
```

### 4.3 双语对应规则

| 规则 | 说明 | 示例 |
|------|------|------|
| **一一配对** | 每个 EN 页面对应一个 ZH 页面 | `en/about.html` ↔ `zh/about.html` |
| **内容对等** | 核心信息保持一致 | 关键数据、结论不遗漏 |
| **本地化** | 非直译，考虑文化差异 | 例子、比喻本地化 |
| **无对应回退** | 无 EN 对应的 ZH 页面，hreflang 指向父级 | `zh/kol/ranking.html` → `en/kol/` |

---

## 五、技术架构

### 5.1 部署平台

- **平台**: Vercel
- **域名**: `pred101.com` / `www.pred101.com`
- **部署方式**: Git push 自动部署
- **预览环境**: 每个 PR 生成独立预览 URL

### 5.2 构建流程

```
Git Push → Vercel Build → HTML/CSS/JS → CDN 分发 → 全球访问
```

### 5.3 自动化脚本

| 脚本 | 功能 | 频率 |
|------|------|------|
| `auto-daily-report.sh` | 生成日报 | 每日 |
| `verify-plan-b.sh` | 验证双语结构 | 每 15 分钟 |
| `fix-missing-en-counterparts.py` | 修复缺失的 EN 对应页 | 按需 |
| `fix-hreflang-mismatch.py` | 修复 hreflang 不匹配 | 按需 |

### 5.4 Cron 配置

**Job ID**: `460c5abf-a1ea-4d54-8068-5d6b12a96fcc`  
**名称**: `pred101-phase2-autopilot-15m`  
**频率**: 每 15 分钟  
**功能**: 自动验证 Phase-2 Plan B 状态

---

## 六、质量检查

### 6.1 每周六全面检查

**执行人**: Zorro-Ops  
**时间**: 每周六 09:00 JST  
**范围**: 全部 110 页

**检查项**:
1. 跳转与导航（语言切换器、内部链接、Canonical/Hreflang）
2. 语言对应（内容纯净度、内容对应）
3. 视觉效果（双层视觉、组件统一、响应式、颜色系统）
4. 功能（搜索、表单、交互元素）
5. 性能（加载速度、资源优化）
6. SEO（Meta 标签、结构化数据、Sitemap）

### 6.2 问题汇报流程

1. Zorro-Ops 执行检查 → 记录问题
2. 在 `#ops` Discord 频道汇报
3. Zorro (main) 接收并修复
4. Zorro-Ops 验证修复结果

### 6.3 问题优先级

| 级别 | 标准 | 响应时间 |
|------|------|----------|
| 🔴 严重 | 影响核心功能（链接失效、内容错误） | 24 小时内 |
| 🟡 中等 | 影响体验但可使用（样式问题、小错误） | 1 周内 |
| 🟢 轻微 | 优化建议（文字润色、视觉微调） | 2 周内 |

---

## 七、数据与 API

### 7.1 数据源

| 数据源 | 用途 | 状态 |
|--------|------|------|
| **Simmer API** | Polymarket 市场数据 | ⚠️ 需配置 API Key |
| **X/Twitter API** | 热门讨论抓取 | ✅ auth_token + ct0 |
| **Reddit API** | 社区讨论 | ⚠️ 偶有 DDoS 限制 |
| **CoinDesk RSS** | 行业新闻 | ✅ 正常 |
| **Polymarket Blog** | 官方公告 | ✅ 正常 |

### 7.2 日报数据结构

```json
{
  "date": "2026-03-16",
  "market_summary": {...},
  "top_markets": [...],
  "twitter_mentions": [...],
  "news": [...],
  "insights": [...]
}
```

### 7.3 周报数据结构

```json
{
  "week": "2026-W12",
  "performance": {...},
  "strategy_returns": [...],
  "market_analysis": {...},
  "key_events": [...]
}
```

---

## 八、访问权限

### 8.1 GitHub 仓库

- **URL**: `https://github.com/robinzorro/pred101`（待确认）
- **分支**: `main`（生产分支）
- **访问权限**: 
  - Zorro (main): 读写
  - Zorro-Research: 读写
  - Zorro-Ops: 读写

### 8.2 Vercel 项目

- **项目名**: `pred101`
- **生产环境**: `https://www.pred101.com`
- **预览环境**: `https://pred101-*.vercel.app`

### 8.3 Discord 频道

| 频道 | 用途 | 成员 |
|------|------|------|
| `#core` | 主沟通频道 | Robin, Zorro |
| `#research` | Zorro-Research 工作 | Zorro-Research |
| `#ops` | Zorro-Ops 工作 | Zorro-Ops |

---

## 九、变更历史

| 版本 | 日期 | 变更内容 | 负责人 |
|------|------|----------|--------|
| 1.0 | 2026-03-16 | 初始版本，包含 Phase-2 Plan B + Phase-3 P0 | Zorro |

---

## 十、附录

### A. 常用命令

```bash
# 本地预览
cd /home/zqd/.openclaw/workspace/polymarket-reporter
python -m http.server 8000

# 验证双语结构
./verify-plan-b.sh

# 检查 EN 路径中文残留
./check-en-pages.sh

# Git 操作
git status
git add .
git commit -m "fix: [描述]"
git push origin main
```

### B. 关键文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| 验证脚本 | `verify-plan-b.sh` | 自动验证双语结构 |
| Vercel 配置 | `vercel.json` | 路由重定向规则 |
| 站点地图 | `sitemap.xml` | SEO 站点地图 |
| 状态报告 | `PHASE2-PLAN-B-FINAL-STATUS.md` | 最新状态汇总 |

### C. 联系人与支持

- **产品负责人**: Robin
- **执行 Agent**: Zorro (main)
- **研究 Agent**: Zorro-Research
- **运维 Agent**: Zorro-Ops

---

**文档结束**
