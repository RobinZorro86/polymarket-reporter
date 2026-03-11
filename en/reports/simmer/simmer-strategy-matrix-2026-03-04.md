# 🎯 Simmer 套利策略配置矩阵（组合 A）

**生成时间：** 2026-03-04 15:35:00 (Asia/Tokyo)  
**版本：** 1.0  
**执行模式：** PAPER MODE（模拟交易）  
**目标：** 胜率≥70%，连续 20 笔正收益后切换实盘

---

## 📊 策略组合总览

| 策略 | 优先级 | 角色 | 扫描频率 | 单笔金额 |
|------|--------|------|----------|----------|
| **Mert Sniper** | P1 | 高频主引擎 | 每 5 分钟 | $8-15 |
| **Weather Trader** | P2 | 稳健底仓 | 每 30 分钟 | $5-12 |
| **Copytrading 过滤版** | P3 | 补充稳定样本 | 每 4 小时 | $5-10 |

**综合优先级：9.1/10**

---

## 1️⃣ Mert Sniper（高频主引擎）

### 核心参数
```bash
export SIMMER_MERT_FILTER="btc,eth,sol,crypto"
export SIMMER_MERT_MAX_BET=12.00
export SIMMER_MERT_EXPIRY_MINS=120
export SIMMER_MERT_MIN_SPLIT=0.62
export SIMMER_MERT_MAX_TRADES=5
export SIMMER_MERT_SIZING_PCT=0.05
```

### 定时任务
```bash
# 每 5 分钟扫描一次
*/5 * * * * cd /Users/arielhe/.openclaw/workspace/skills/polymarket-mert-sniper && python3 mert_sniper.py >> /tmp/mert_sniper.log 2>&1
```

### 触发条件（必须同时满足）
- ✅ 市场到期时间 ≤ 120 分钟
- ✅ 赔率倾斜 ≥ 62%/38%
- ✅ 市场流动性充足（bid-ask spread < 5%）
- ✅ 无冲突持仓（check_conflict 返回 false）

### 停机条件（任一触发即停机）
- ❌ 连续亏损 3 笔
- ❌ 单日亏损 ≥ $25
- ❌ 市场异常（价格 > 0.98 或 < 0.02）

### 风控配置
| 指标 | 阈值 |
|------|------|
| 单笔最大 | $15 |
| 单日最大 | $50 |
| 连续亏损停机 | 3 笔 |
| 冷却时间 | 30 分钟 |
| 极端价位禁止 | >0.95 或 <0.05 |

---

## 2️⃣ Weather Trader（稳健底仓）

### 核心参数
```bash
export SIMMER_WEATHER_ENTRY=0.12
export SIMMER_WEATHER_EXIT=0.45
export SIMMER_WEATHER_MAX_POSITION=10.00
export SIMMER_WEATHER_LOCATIONS="NYC,Chicago,Seattle,Atlanta,Dallas,Miami"
export SIMMER_WEATHER_MAX_TRADES=5
export TRADING_VENUE=simmer
```

### 定时任务
```bash
# 每 30 分钟扫描一次
*/30 * * * * cd /Users/arielhe/.openclaw/workspace/skills/polymarket-weather-trader && python3 weather_trader.py >> /tmp/weather_trader.log 2>&1
```

### 触发条件（必须同时满足）
- ✅ NOAA 预报概率 ≥ 70%
- ✅ 市场隐含概率 ≤ 45%
- ✅ 边缘优势 `edge >= 12%`
- ✅ 市场流动性充足

### 停机条件（任一触发即停机）
- ❌ 连续亏损 5 笔
- ❌ 单日亏损 ≥ $30
- ❌ NOAA 数据源异常

### 风控配置
| 指标 | 阈值 |
|------|------|
| 单笔最大 | $12 |
| 单日最大 | $40 |
| 连续亏损停机 | 5 笔 |
| 冷却时间 | 1 小时 |
| 止盈目标 | 35%+ |
| 止损阈值 | -15% |

---

## 3️⃣ Copytrading 过滤版（补充稳定样本）

### 核心参数
```bash
export SIMMER_COPYTRADING_TOP_N=5
export SIMMER_COPYTRADING_MIN_WINRATE=0.62
export SIMMER_COPYTRADING_MAX_POSITION=10.00
export SIMMER_COPYTRADING_REBALANCE_THRESHOLD=0.15
export SIMMER_COPYTRADING_EXCLUDE_WALLETS=""
```

### 定时任务
```bash
# 每 4 小时扫描一次
0 */4 * * * cd /Users/arielhe/.openclaw/workspace/skills/polymarket-copytrading && python3 copytrading_trader.py >> /tmp/copytrading.log 2>&1
```

### 筛选条件（必须同时满足）
- ✅ 目标钱包最近 30 天胜率 > 62%
- ✅ 目标钱包最大回撤可控（< 25%）
- ✅ 非单一主题赌徒型钱包
- ✅ 持仓分散度达标（单一市场≤30%）

### 停机条件（任一触发即停机）
- ❌ 跟单钱包连续亏损 5 笔
- ❌ 单日亏损 ≥ $20
- ❌ 目标钱包策略漂移

### 风控配置
| 指标 | 阈值 |
|------|------|
| 单笔最大 | $10 |
| 单日最大 | $30 |
| 单钱包敞口上限 | 总仓 25% |
| 最大跟单钱包数 | 5 个 |
| 再平衡阈值 | 15% 偏离 |

---

## 🛡️ 统一风控模板（Aegis v2 风格）

### 账户级风控
```bash
# 总账户限制
export ACCOUNT_MAX_DAILY_LOSS=50.00
export ACCOUNT_MAX_POSITION_SIZE=15.00
export ACCOUNT_MAX_CONCURRENT_POSITIONS=10
export ACCOUNT_CIRCUIT_BREAKER_LOSSES=3
export ACCOUNT_COOLDOWN_MINUTES=30
```

### 执行前检查清单
1. ✅ 检查账户余额是否充足
2. ✅ 检查是否有冲突持仓
3. ✅ 检查市场状态（是否暂停/结算中）
4. ✅ 检查滑点是否在容忍范围内
5. ✅ 检查今日亏损是否超限

### 执行后监控
1. 📊 实时跟踪持仓 P&L
2. 📊 监控市场赔率变化
3. 📊 触发止盈止损自动执行
4. 📊 记录每笔交易日志

---

## 📈 监控与报告

### 日志位置
| 策略 | 日志文件 | 实时查看命令 |
|------|----------|--------------|
| Mert Sniper | `/tmp/mert_sniper.log` | `tail -f /tmp/mert_sniper.log` |
| Weather Trader | `/tmp/weather_trader.log` | `tail -f /tmp/weather_trader.log` |
| Copytrading | `/tmp/copytrading.log` | `tail -f /tmp/copytrading.log` |

### 每日报告指标
- 总交易笔数
- 胜率（%）
- 总 P&L（$SIM）
- 最大回撤
- 夏普比率
- 各策略贡献度

### 周度复盘
- 策略表现对比
- 参数优化建议
- 风险事件回顾
- 下周调整计划

---

## 🎯 毕业标准（模拟→实盘）

### 必须同时满足
1. ✅ 胜率 ≥ 70%（至少 50 笔样本）
2. ✅ 连续 20 笔正收益
3. ✅ 最大回撤 < 15%
4. ✅ 夏普比率 > 1.5
5. ✅ 无重大风控违规

### 实盘切换步骤
1. 往 Simmer 钱包充值 $50-100 USDC.e
   - 地址：`0x86E26b79a6F845fd1a11fc704c68486E03920214`
2. 修改环境变量 `TRADING_VENUE=polymarket`
3. 设置 `WALLET_PRIVATE_KEY`（如用自托管）
4. 执行 `client.set_approvals()` 授权合约
5. 切换到 `--live` 模式
6. 首周单笔上限 $10，观察执行质量

---

## 📅 执行时间表

| 阶段 | 时间 | 目标 |
|------|------|------|
| **配置落地** | Day 0（今天） | 完成所有参数设置 + 定时任务 |
| **模拟运行** | Day 1-7 | 累积数据，优化参数 |
| **中期复盘** | Day 7 | 检查胜率/回撤，调整参数 |
| **继续模拟** | Day 8-14 | 巩固胜率，冲刺毕业标准 |
| **实盘切换** | Day 14+ | 达标后切换，小金额测试 |

---

## 🔧 快速命令参考

### 查看状态
```bash
# 检查定时任务
crontab -l

# 查看各策略日志
tail -f /tmp/mert_sniper.log
tail -f /tmp/weather_trader.log
tail -f /tmp/copytrading.log

# 查看 Simmer 账户余额
cd skills/simmer && python3 scripts/status.py
```

### 手动触发
```bash
# 手动运行一次 Mert Sniper
cd skills/polymarket-mert-sniper && python3 mert_sniper.py

# 手动运行 Weather Trader
cd skills/polymarket-weather-trader && python3 weather_trader.py

# 查看持仓
cd skills/simmer && python3 scripts/status.py --positions
```

### 紧急停机
```bash
# 暂停所有定时任务
crontab -r

# 或注释掉特定任务
crontab -e  # 在对应行前加 #
```

---

## 📞 支持资源

| 类型 | 链接 |
|------|------|
| Simmer 官网 | https://simmer.markets |
| SDK 文档 | https://simmer.markets/docs.md |
| 技能市场 | https://simmer.markets/skills |
| Telegram 社区 | https://t.me/+m7sN0OLM_780M2Fl |
| GitHub SDK | https://github.com/SpartanLabsXyz/simmer-sdk |

---

**🤖 由 Jarvis 自动生成**  
**下次更新：** 2026-03-05  
**更新时间戳：** 2026-03-04 15:35:00 (Asia/Tokyo)
