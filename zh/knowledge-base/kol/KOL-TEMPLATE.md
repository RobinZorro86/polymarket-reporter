# KOL 页面标准化模板 (双语)

**版本**: 1.0  
**创建时间**: 2026-03-17 07:00 JST  
**用途**: 统一 12 个 KOL 页面的结构和内容

---

## 📐 页面结构

### 1. Hero 区域
```html
- 标题：@username
- 副标题：一句话定位（系统型/实战型/信息型）
- 元数据网格：
  - 类型：系统型 / 实战型 / 信息型
  - 更新时间：YYYY-MM-DD
  - 适合学习：策略框架 / 执行技巧 / 信息源
  - 研究用途：建立方法论 / 跟单参考 / 信号源
```

### 2. 研究结论
```markdown
- 核心判断：1-2 句总结该 KOL 的核心价值
- 为什么值得学：独特优势
- 标签：3-5 个关键词
```

### 3. 交易原型/策略框架
```markdown
每个策略包含：
- 名称（中英文）
- 核心概念（1 句话）
- 关键 edge（2-3 点）
- 适合人群
- 风险提示（如适用）
```

### 4. 如何使用此页面
```markdown
- 学习建议（3-4 条）
- 不要做什么（1-2 条）
```

### 5. 相关链接
```markdown
- Twitter/X 链接
- 相关策略页面
- 相关资源
```

---

## 📝 内容模板（中文）

```html
<section class="hero">
  <div class="eyebrow">KOL research</div>
  <h1>@{username}</h1>
  <p class="lead">{一句话定位}</p>
  <div class="meta-grid">
    <div class="meta-card"><div class="label">类型</div><div class="value">{类型}</div></div>
    <div class="meta-card"><div class="label">更新</div><div class="value">{更新日期}</div></div>
    <div class="meta-card"><div class="label">适合学习</div><div class="value">{学习方向}</div></div>
    <div class="meta-card"><div class="label">研究用途</div><div class="value">{用途}</div></div>
  </div>
</section>

<section class="section">
  <h2>📌 研究结论</h2>
  <p><strong>核心判断：</strong>{核心判断}</p>
  <div class="note"><strong>为什么值得学：</strong>{理由}</div>
  <div class="tags">
    <span class="tag">{标签 1}</span>
    <span class="tag">{标签 2}</span>
    <span class="tag">{标签 3}</span>
  </div>
</section>

<section class="section">
  <h2>🎯 交易原型/策略框架</h2>
  
  <div class="strategy-card">
    <h3>1. {策略名称}</h3>
    <p class="concept">{核心概念}</p>
    <ul>
      <li><strong>关键 edge：</strong>{edge 要点}</li>
      <li><strong>适合人群：</strong>{人群描述}</li>
    </ul>
  </div>
  
  <!-- 重复 strategy-card 块 -->
</section>

<section class="section">
  <h2>✅ 如何使用这个对象页</h2>
  <ul>
    <li>{建议 1}</li>
    <li>{建议 2}</li>
    <li>{建议 3}</li>
  </ul>
</section>

<section class="section">
  <h2>🔗 相关链接</h2>
  <ul>
    <li><a href="https://x.com/{username}">Twitter / X @{username}</a></li>
    <li><a href="/zh/knowledge-base/strategies/{相关策略}/">{相关策略}</a></li>
  </ul>
</section>
```

---

## 📝 Content Template (English)

```html
<section class="hero">
  <div class="eyebrow">KOL Research</div>
  <h1>@{username}</h1>
  <p class="lead">{One-sentence positioning}</p>
  <div class="meta-grid">
    <div class="meta-card"><div class="label">Type</div><div class="value">{Systematic/Practical/Information}</div></div>
    <div class="meta-card"><div class="label">Updated</div><div class="value">{YYYY-MM-DD}</div></div>
    <div class="meta-card"><div class="label">Best for</div><div class="value">{Learning focus}</div></div>
    <div class="meta-card"><div class="label">Use case</div><div class="value">{Research purpose}</div></div>
  </div>
</section>

<section class="section">
  <h2>📌 Key Insights</h2>
  <p><strong>Core thesis:</strong> {Core insight}</p>
  <div class="note"><strong>Why follow:</strong> {Unique value proposition}</div>
  <div class="tags">
    <span class="tag">{Tag 1}</span>
    <span class="tag">{Tag 2}</span>
    <span class="tag">{Tag 3}</span>
  </div>
</section>

<section class="section">
  <h2>🎯 Trading Archetypes / Strategy Framework</h2>
  
  <div class="strategy-card">
    <h3>1. {Strategy Name}</h3>
    <p class="concept">{Core concept}</p>
    <ul>
      <li><strong>Key edge:</strong> {Edge points}</li>
      <li><strong>Best for:</strong> {Target audience}</li>
    </ul>
  </div>
  
  <!-- Repeat strategy-card blocks -->
</section>

<section class="section">
  <h2>✅ How to Use This Profile</h2>
  <ul>
    <li>{Recommendation 1}</li>
    <li>{Recommendation 2}</li>
    <li>{Recommendation 3}</li>
  </ul>
</section>

<section class="section">
  <h2>🔗 Related Links</h2>
  <ul>
    <li><a href="https://x.com/{username}">Twitter / X @{username}</a></li>
    <li><a href="/en/knowledge-base/strategies/{related-strategy}/">{Related Strategy}</a></li>
  </ul>
</section>
```

---

## 📋 12 位 KOL 清单

| # | Username | 类型 | 核心策略 | 优先级 |
|---|----------|------|----------|--------|
| 1 | vladic_eth | 系统型 | 信息套利 + 做市 + 鲸鱼跟踪 | P0 |
| 2 | noisyb0y1 | 实战型 | Fast-Loop 高频 | P0 |
| 3 | RohOnChain | 信息型 | 事件驱动 | P1 |
| 4 | AYi_AInotes | 信息型 | AI/新闻流 | P1 |
| 5 | DmitriyUngarov | | | P2 |
| 6 | edwordkaru | | | P2 |
| 7 | aleiahlock | | | P2 |
| 8 | cutnpaste4 | | | P2 |
| 9 | molt-cornelius | | | P2 |
| 10 | runic-leo | | | P2 |
| 11 | 0xchainmind | | | P2 |
| 12 | rankings | 排名页 | N/A | P0 |

---

## ✅ 执行步骤

1. 以 `vladic_eth` 为模板（已存在）
2. 为其他 11 个 KOL 创建相同结构页面
3. 确保中英文版本配对
4. 添加排名页 (`rankings/index.html`)

---

**下一步**: 开始批量创建 KOL 页面
