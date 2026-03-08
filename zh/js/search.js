// Musk Collective 站内搜索
// 纯前端实现，无需服务器

const searchIndex = [
  // KOL 策略
  {
    title: "@zstmfhy - AI 记忆增强生态系统",
    description: "Supermemory 85.9% 召回率，Graph Memory 新趋势",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["记忆系统", "Supermemory", "mem0", "Graph Memory"]
  },
  {
    title: "@AYi_AInotes - OpenClaw Workflow 交易策略",
    description: "趋势交易、价值投资、套利策略完整指南",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["OpenClaw", "Workflow", "自动化交易"]
  },
  {
    title: "@cutnpaste4 - Crypto Up/Down 市场完全指南",
    description: "延迟套利真相、定价模型、Maker vs Taker 策略对比",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["加密货币", "延迟", "做市", "Maker", "Taker"]
  },
  {
    title: "@RohOnChain - 对冲基金预测市场数据方法论",
    description: "400M 交易数据、经验 Kelly、Monte Carlo 重采样",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["对冲基金", "数据驱动", "Kelly", "Monte Carlo", "Maker/Taker"]
  },
  {
    title: "@seanzhao1105 - 109GB 价差套利复盘",
    description: "99.99% 人不适合、2 秒延迟陷阱",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["套利", "数据复盘", "延迟"]
  },
  {
    title: "@edwordkaru - Simmer 自动交易教程",
    description: "旧手机 + OpenClaw + Simmer 自动交易完整教程",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["OpenClaw", "Simmer", "自动交易", "Weather Trader"]
  },
  {
    title: "@noisyb0y1 - 套利策略系列",
    description: "Fast-Loop、5 分钟 BTC、Clawdbot 跟单、钱包追踪",
    url: "/knowledge-base/kol-strategies.html",
    tags: ["Fast-Loop", "套利", "机器人", "+$386K/月"]
  },
  // 系统架构
  {
    title: "Aegis V2 系统架构",
    description: "7 层架构：数据→信号→决策→执行→风控→运维",
    url: "/knowledge-base/aegis-system/architecture.html",
    tags: ["系统架构", "Aegis", "V2"]
  },
  {
    title: "Aegis V2 项目里程碑",
    description: "6 阶段开发计划与当前进度",
    url: "/knowledge-base/aegis-system/milestones.html",
    tags: ["里程碑", "项目进度", "Aegis"]
  },
  // 工具资源
  {
    title: "工具资源汇总",
    description: "OpenClaw、polymarket-cli、Simmer、Chainstack",
    url: "/knowledge-base/tools-resources.html",
    tags: ["工具", "OpenClaw", "CLI"]
  },
  // 风险管理
  {
    title: "风险管理",
    description: "风控、止损、熔断机制",
    url: "/knowledge-base/risk-management.html",
    tags: ["风控", "止损", "熔断", "风险"]
  },
  // 报告
  {
    title: "Polymarket 日报",
    description: "每日资讯聚合 (隔天 09:00 更新)",
    url: "/reports/",
    tags: ["日报", "资讯", "每日更新"]
  },
  {
    title: "Polymarket 周报",
    description: "每周核心事件汇总 (每周一 09:00 更新)",
    url: "/reports/",
    tags: ["周报", "每周更新"]
  }
];

// 搜索函数
function search(query) {
  if (!query || query.trim().length < 2) {
    return [];
  }
  
  const q = query.toLowerCase().trim();
  
  return searchIndex.filter(item => {
    const title = item.title.toLowerCase();
    const desc = item.description.toLowerCase();
    const tags = item.tags.join(' ').toLowerCase();
    
    return title.includes(q) || desc.includes(q) || tags.includes(q);
  });
}

// 渲染搜索结果
function renderResults(results, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  if (results.length === 0) {
    container.innerHTML = '<p style="color: #64748b; padding: 20px;">未找到相关内容</p>';
    return;
  }
  
  container.innerHTML = results.map(item => `
    <a href="${item.url}" class="report-card" style="text-decoration: none; display: block; margin-bottom: 12px;">
      <div class="title" style="font-weight: 600; color: #1e293b; margin-bottom: 4px;">${item.title}</div>
      <div class="meta" style="color: #64748b; font-size: 0.875rem;">${item.description}</div>
      <div class="tags" style="margin-top: 8px;">
        ${item.tags.map(tag => `<span style="font-size: 0.75rem; padding: 2px 8px; background: #f1f5f9; border-radius: 4px; color: #64748b; margin-right: 4px;">${tag}</span>`).join('')}
      </div>
    </a>
  `).join('');
}

// 初始化搜索
function initSearch(inputId, resultsId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  
  let debounceTimer;
  
  input.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = e.target.value;
      if (query.length >= 2) {
        const results = search(query);
        renderResults(results, resultsId);
        document.getElementById(resultsId).style.display = 'block';
      } else {
        document.getElementById(resultsId).style.display = 'none';
      }
    }, 300);
  });
}

// 导出到全局
window.MuskCollective = {
  search,
  renderResults,
  initSearch
};