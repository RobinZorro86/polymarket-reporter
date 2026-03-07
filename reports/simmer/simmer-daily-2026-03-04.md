# 📊 Polymarket 特别日报（Simmer 篇）
**日期：2026 年 3 月 4 日** | **版本：1.0**

---

## 🎯 一、Simmer 核心定位

**Simmer** 是专为 AI Agent 设计的预测市场交易接口，由 **Spartan Labs** 开发。

| 特性 | 说明 |
|------|------|
| **目标用户** | AI 自主交易 Agent（也支持手动交易） |
| **支持市场** | Polymarket（Polygon）、Kalshi |
| **钱包模式** | 自托管钱包（Self-Custody）或 Simmer 托管 |
| **模拟交易** | $SIM 虚拟货币，真实市场价格，零风险练习 |
| **统一 API** | 一个 SDK 接入多个交易场所 |

**官网：** https://simmer.markets  
**SDK 文档：** https://simmer.markets/docs.md  
**Telegram 社区：** https://t.me/+m7sN0OLM_780M2Fl

---

## 🧠 二、策略体系（4 大核心策略）

### 1️⃣ Weather Trader（天气交易）
**灵感来源：** @gopfan2 的温度预测策略

| 项目 | 配置 |
|------|------|
| **数据源** | NOAA 天气预报 API |
| **策略逻辑** | 当预报显示强边缘（如 70%+ 概率）vs 市场隐含概率（如 40%）时买入 |
| **出场条件** | 赔率收敛或达到利润目标 |
| **适用市场** | Polymarket 温度预测市场 |
| **安装命令** | `clawhub install polymarket-weather-trader` |

**核心代码逻辑：**
```python
# 比较 NOAA 预报 vs 市场价格
if forecast_probability >= 0.70 and market_implied <= 0.40:
    buy_yes_shares(amount=10.0)
```

---

### 2️⃣ Mert Sniper（到期狙击）
**灵感来源：** @mert 的临近到期 conviction 交易策略

| 项目 | 配置 |
|------|------|
| **扫描窗口** | 默认 2-8 分钟内到期 |
| **最小倾斜** | 60%/40% 或更高 |
| **最大仓位** | $10/笔（可配置） |
| **适用市场** | 5 分钟加密货币市场（BTC/ETH/SOL 涨跌） |
| **安装命令** | `clawhub install polymarket-mert-sniper` |

**策略特点：**
- 只在市场即将结算时下注
- 只选择赔率高度倾斜的市场（一边≥60%）
- 跟随高概率方向

**配置示例：**
```bash
export SIMMER_MERT_EXPIRY_MINS=120
export SIMMER_MERT_MIN_SPLIT=0.60
export SIMMER_MERT_MAX_BET=10.00
```

---

### 3️⃣ Copytrading（跟单策略）
**功能：** 自动追踪并复制成功交易员的持仓

| 项目 | 配置 |
|------|------|
| **追踪对象** | Top-N 高胜率钱包 |
| **最小跟单金额** | 可配置（如$5 起） |
| **再平衡逻辑** | 自动计算目标配置并执行调仓 |
| **安装命令** | `clawhub install polymarket-copytrading` |

**工作流程：**
1. 扫描缺失的市场
2. 应用 Top-N 和最小规模规则
3. 计算再平衡交易以匹配目标配置
4. 通过 Simmer 执行交易（遵守支出和最小份额限制）

---

### 4️⃣ Signal Sniper（信号狙击）
**功能：** 基于 RSS 订阅源自动交易

| 项目 | 配置 |
|------|------|
| **数据源** | RSS 订阅（新闻、推特、博客等） |
| **触发条件** | 关键词匹配 + 情绪分析 |
| **执行速度** | 秒级响应 |
| **安装命令** | `clawhub install polymarket-signal-sniper` |

---

## 📚 三、教程与实操路径

### 阶段 1：模拟交易（$SIM）
**目标：** 在零风险环境下累积交易数据和经验

```bash
# 1. 获取 API Key
访问 https://simmer.markets/dashboard → SDK 标签页

# 2. 设置环境变量
export SIMMER_API_KEY=sk_live_xxx
export TRADING_VENUE=simmer  # 模拟模式

# 3. 安装技能
clawhub install polymarket-weather-trader
clawhub install polymarket-mert-sniper

# 4. 运行模拟
cd skills/polymarket-weather-trader
python3 weather_trader.py  # 默认 dry-run
```

**毕业标准：** 胜率≥70%，连续 20 笔交易正收益

---

### 阶段 2：真实交易（Polymarket）
**前提：** 模拟阶段达到毕业标准

```bash
# 1. 充值 USDC.e 到 Simmer 钱包
地址：0x86E26b79a6F845fd1a11fc704c68486E03920214
（或配置自己的 WALLET_PRIVATE_KEY）

# 2. 切换到真实模式
export TRADING_VENUE=polymarket
export WALLET_PRIVATE_KEY=0x...  # 自托管钱包需要

# 3. 开启真实交易
python3 weather_trader.py --live
```

**⚠️ 重要提醒：**
- 首次真实交易前需执行 `client.set_approvals()` 授权合约
- 真实市场有 2-5% 订单簿滑差，$SIM 无滑差
- 建议从$10-20 小额开始测试

---

### 阶段 3：多策略并行
**配置：** 同时运行多个策略，分散风险

```bash
# 定时任务示例（每 5 分钟扫描）
*/5 * * * * cd /path/to/skills && python3 mert_sniper.py --live >> /tmp/mert.log
*/5 * * * * cd /path/to/skills && python3 weather_trader.py --live >> /tmp/weather.log
```

---

## 🔥 四、社媒热点与讨论

### X/Twitter 高互动内容
| 账号 | 内容摘要 | 互动 |
|------|----------|------|
| @TheSpartanLabs | 发布 Polymarket 交易技能原型：Weather Trader / Copytrading / Signal Sniper | 高 |
| @meta8mate | OpenClaw 多 Agent × TG 群组自动化系统配置教程 | 309 喜欢 / 139 转帖 |
| @Berryxia.AI | OpenClaw 养成记：40 天实战经验 + 文件架构体系 | 589 喜欢 / 168 转帖 |

### 关键讨论点
1. **多 Agent 协作模式**：基于文件的 STATE.yaml 去中心化协作，省 Token 80%
2. **模拟→实盘路径**：先用$SIM 累积数据，胜率 70% 后再开启真实交易
3. **配置陷阱**：子 Agent 默认不能互相通信，需开启 `sessions.visibility: all`

---

## 💬 五、Reddit 热帖与讨论趋势

**r/Polymarket 搜索结果：** 暂无直接提及"Simmer"的热帖  
**r/CryptoCurrency 相关讨论：**
- Weather Trading Bots  quiet making $24,000 on Polymarket（Dev Genius，3 周前）
- 核心观点：使用 OpenClaw + Simmer SDK 可零代码部署全自动交易机器人

---

## ⚠️ 六、风险与注意事项

### 1. 钱包安全
| 风险 | 建议 |
|------|------|
| 私钥泄露 | 使用专用小号钱包，不要放主力资金 |
| Simmer 托管 | 服务器端管理密钥，存在平台风险 |
| 自托管钱包 | 需自行保管私钥，丢失无法恢复 |

### 2. 交易风险
| 风险 | 建议 |
|------|------|
| 滑点 | 真实市场有 2-5% 订单簿滑差，$SIM 无滑差 |
| 流动性 | 小市场可能无法及时成交 |
| 结算延迟 | Polymarket 结算依赖预言机，可能延迟 |

### 3. 配置陷阱
| 问题 | 解决方案 |
|------|----------|
| Gateway 重启 = 缓存清空 | 改配置务必备份，一次到位 |
| 子 Agent 无法通信 | 开启 `tools.sessions.visibility: all` |
| Subagent 超时 | 调长等待响应时间 |
| TG 菜单项过多报错 | 关闭子 Agent 的 `commands.native` |

---

## ✅ 七、可执行建议（针对你的账户）

### 当前状态
| 项目 | 状态 |
|------|------|
| SIMMER_API_KEY | ✅ 已配置 |
| WALLET_PRIVATE_KEY | ❌ 未设置 |
| Simmer 钱包地址 | `0x86E26b79a6F845fd1a11fc704c68486E03920214` |
| 交易模式 | **PAPER MODE（模拟）** |
| 已安装技能 | 12 个（包括 Weather/Mert/Copytrading 等） |

### 今日动作清单
1. **继续模拟交易练习**
   - 已设置 Mert Sniper 每 5 分钟扫描一次
   - 日志位置：`/tmp/mert_sniper.log`

2. **充值 USDC.e（可选）**
   - 往 Simmer 钱包充值$10-20 测试真实交易
   - 使用 Across Bridge (https://across.to) 从其他链跨过来

3. **监控模拟交易数据**
   - 目标：胜率≥70%，连续 20 笔正收益
   - 达到标准后再开启真实交易

4. **配置多策略并行（进阶）**
   - 同时运行 Weather Trader + Mert Sniper
   - 分散风险，提高收益稳定性

---

## 📎 附录：资源链接

| 类型 | 链接 |
|------|------|
| 官网 | https://simmer.markets |
| SDK 文档 | https://simmer.markets/docs.md |
| 技能市场 | https://simmer.markets/skills |
| ClawHub | https://clawhub.ai |
| Telegram | https://t.me/+m7sN0OLM_780M2Fl |
| GitHub SDK | https://github.com/SpartanLabsXyz/simmer-sdk |

---

**🤖 由 Jarvis 自动生成** | **下次更新：2026-03-05**
