# pred101.com Design Spec — 2026-04-01

## 1. 背景与目标

对 pred101.com 全站进行设计升级，遵循 frontend-design skill 的设计理念：
**避免 AI 通用感，做出有记忆点的专业感**。

目标：
- 建立统一的 CSS 设计系统，替换内联样式
- 提升首页和主要落地页的视觉冲击力
- 保持功能纯粹，不为设计牺牲可读性和可用性

---

## 2. 美学方向

**方向名称：Dark Terminal Editorial**
暗色终端感 + 金融社论风格的混合。

**适用场景**：预测市场 / Web3 / 数据交易人群
**关键词**：专业、数据感、不平庸、有记忆点

**设计方向详解**：
- 深色背景（不是纯黑，带微妙的蓝/紫底色）
- 亮色数据点缀（不是紫色渐变，用更冷的青/琥珀对比）
- 大字体标题（editorial 感的衬线或半衬线）
- 卡片带玻璃态光泽 + 细边框
- 细节丰富但克制：不为炫技，细节服务于信息层级

---

## 3. 色彩系统

```css
:root {
  /* 背景层次 */
  --bg-deep:     #07090f;   /* 最深背景 */
  --bg-base:     #0b1020;   /* 页面主背景 */
  --bg-surface:  #111827;   /* 卡片/面板背景 */
  --bg-elevated: #1a2338;  /* 悬停/高亮态 */

  /* 边框 */
  --border:       rgba(148, 163, 184, 0.10);
  --border-strong: rgba(148, 163, 184, 0.22);

  /* 文字 */
  --text-primary:   #f1f5f9;  /* 主文字 */
  --text-secondary: #94a3b8;  /* 次要文字 */
  --text-muted:     #475569;  /* 弱文字 */

  /* 强调色 */
  --accent-cyan:   #22d3ee;  /* 主强调（青） */
  --accent-amber:  #fbbf24;  /* 次强调（琥珀） */
  --accent-violet: #a78bfa;  /* 第三强调（紫） */

  /* 语义色 */
  --positive: #34d399;  /* 涨/正确 */
  --negative: #f87171;  /* 跌/错误 */
  --warning:  #fbbf24;  /* 警告 */

  /* 特效 */
  --glow-cyan:   0 0 24px rgba(34, 211, 238, 0.20);
  --glow-amber:  0 0 24px rgba(251, 191, 36, 0.20);
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.40);
}
```

---

## 4. 字体系统

**Display / 标题字体**：
- `Instrument Serif` (Google Fonts) — 有个性的衬线，用于 hero 大标题
- 回退：`Georgia`, `serif`

**Body / 正文字体**：
- `DM Sans` (Google Fonts) — 现代几何无衬线，可读性好
- 回退：`system-ui`, `sans-serif`

**数据 / 等宽字体**：
- `JetBrains Mono` (Google Fonts) — 用于数字、代码、价格
- 回退：`monospace`

```css
font-family: 'Instrument Serif', Georgia, serif;       /* 标题 */
font-family: 'DM Sans', system-ui, sans-serif;        /* 正文 */
font-family: 'JetBrains Mono', monospace;              /* 数据 */
```

---

## 5. 动效规范

**入场动画（页面加载）**：
- 元素 opacity 0→1，配合 translateY(16px)→0
- 持续 500ms，ease-out
- 标题先出，卡片依次延迟 80ms 一张

**滚动触发动画**：
- Intersection Observer 检测
- 元素进入视口时触发动画
- 卡片错开 60ms 入场

**悬停效果**：
- 卡片：边框变亮 + 微弱发光（--glow-cyan）+ translateY(-3px)
- 按钮：背景色微亮 + 边框变强
- 时间：200ms ease

**禁止项**：
- 不过度使用紫色/蓝色渐变背景
- 不用 Inter / Roboto / Arial / Space Grotesk
- 不做纯装饰无意义的动画
- 不使用 emoji 作为主要图标（改用 SVG 或 CSS shape）

---

## 6. 布局节奏

**页面宽度**：`max-width: 1200px`，内容区 1180px
**栅格**：12列系统，卡片通常占 3/4/6 列
**间距基准**：8px 网格（8, 16, 24, 32, 48, 64, 96px）

**Hero 区域**（首页顶部）：
- 超大标题（clamp 3.5rem - 6rem）
- 副标题 + CTA 按钮组
- 右侧可选：数据指标卡 / 最新报告预览

**Section 区域**：
- 标题 + 描述 + 卡片网格
- 卡片不等高时底部对齐（align-items: stretch）

**报告页面**：
- 侧边导航（TOC）或单栏沉浸阅读
- 报告头部带日期、类型标签

---

## 7. 卡片设计

```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-card);
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
.card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-card), var(--glow-cyan);
  transform: translateY(-3px);
}
```

---

## 8. 导航设计

**Header（ sticky）**：
- 背景：`rgba(7, 9, 15, 0.80)` + `backdrop-filter: blur(20px)`
- 高度：64px
- Logo：左对齐，白色文字，"pred101" 部分用 `--accent-cyan`
- Nav 链接：间距 28px，当前页下划线高亮
- 语言切换：胶嚢形开关（EN / 中文）

**Footer**：
- 简洁单行：Logo + 导航链接 + 版权
- 上边框：`1px solid var(--border)`

---

## 9. 页面优先级

### Phase 1 — 高优先级（门户页）
1. `zh/index.html` — 主站首页（最重要）
2. `en/index.html` — 英文首页
3. `zh/knowledge-base/index.html` — 知识库索引
4. `zh/learn/index.html` — 学习路径索引
5. `zh/kol/index.html` — KOL 评估页
6. `zh/reports/index.html` — 报告索引页
7. `zh/resources/index.html` — 资源中心

### Phase 2 — 中优先级（功能页）
8. `zh/about.html` — 关于页
9. `en/learn/index.html` — 英文学习索引
10. `en/knowledge-base/index.html` — 英文知识库
11. `en/kol/index.html` — 英文 KOL
12. `en/reports/index.html` — 英文报告索引

### Phase 3 — 低优先级（内容页）
- 日报 / 周报详情页（批量处理）
- 学习日页面（day1-7）
- 知识库子页面（strategies, resources, tutorials）
- KOL 子页面

---

## 10. 技术约束

- 纯 HTML + CSS + Vanilla JS（不引入框架）
- 所有新样式写入 `css/redesign.css`，各页通过 `<link>` 引用
- 共享 header/footer HTML 通过 JS 组件化（`components/header.js`）
- CSS 变量集中管理，新页面通过 class 名引用
- 字体通过 Google Fonts CDN 引入（预连接优化）
- 保持现有 HTML 结构不变，只替换/增强 `<style>` 块和 CSS 类

---

## 11. 验收标准

- [ ] 无紫色/蓝色渐变背景（用深色 + 强调色点缀代替）
- [ ] 字体使用 Instrument Serif / DM Sans / JetBrains Mono
- [ ] 卡片有 hover 发光效果（青光）
- [ ] 首页有页面加载入场动画（staggered reveal）
- [ ] 导航 header sticky + 毛玻璃效果
- [ ] 移动端响应式（768px / 1024px 两个断点）
- [ ] 数字/价格使用等宽字体
- [ ] 无 emoji 作为唯一图标（用 SVG 或 CSS shape 替代）
