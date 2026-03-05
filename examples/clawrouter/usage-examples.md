# ClawRouter 使用示例

## 1. 基础命令

### 查看钱包状态
```
/wallet
```

### 查看使用统计
```
/stats
```

## 2. 切换路由策略

### 均衡模式（默认）
```
/model auto
```
- 74-100% 节省
- 适用于通用任务

### 节能模式
```
/model eco
```
- 95-100% 节省
- 适用于简单任务

### 高质量模式
```
/model premium
```
- 0% 节省
- 适用于关键任务

### 免费模式
```
/model free
```
- 100% 免费
- 使用 gpt-oss-120b

## 3. 快捷模型选择

```
/model grok        # 使用 xAI Grok
/model br-sonnet  # 使用 DeepSeek Sonnet
/model gpt5       # 使用 GPT-5
/model o3         # 使用 OpenAI O3
/model claude     # 使用 Claude Sonnet
```

## 4. 图像生成

### 基本使用
```
/imagegen a cat on the beach
```

### 指定模型和尺寸
```
/imagegen --model dall-e-3 --size 1792x1024 futuristic city
```

### 可用模型
| 命令 | 模型 | 价格 |
|------|------|------|
| `--model nano-banana` | Gemini Flash | $0.05 |
| `--model banana-pro` | Gemini Pro | $0.10 |
| `--model dall-e-3` | DALL-E 3 | $0.04 |
| `--model gpt-image` | GPT Image 1 | $0.02 |
| `--model flux` | Flux 1.1 | $0.04 |

### 尺寸选项
- `--size 1024x1024` (默认)
- `--size 1792x1024` (dall-e-3)
- `--size 2048x2048` (banana-pro)

## 5. 钱包管理

### 切换到 Solana
```
/wallet solana
```

### 切换到 Base
```
/wallet base
```

### 导出钱包（备份）
```
/wallet export
```

## 6. 诊断问题

### 运行诊断
```bash
npx @blockrun/clawrouter doctor
```

### 使用 Opus 深度分析
```bash
npx @blockrun/clawrouter doctor opus
```

### 询问具体问题
```bash
npx @blockrun/clawrouter doctor "为什么我的请求失败了？"
```

## 7. API 调用（高级）

### 通过 cURL 调用

```bash
curl -X POST http://localhost:8402/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "x-model: auto" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "gpt-4o"
  }'
```

### Python 示例

```python
import requests

response = requests.post(
    "http://localhost:8402/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "x-model": "auto"  # 路由策略
    },
    json={
        "messages": [{"role": "user", "content": "Hello!"}],
        "model": "gpt-4o"
    }
)

print(response.json())
```

## 8. 工作流示例

### 成本优化工作流
```
1. /model eco          # 切换到节能模式
2. [简单任务]          # 执行简单任务
3. /model auto        # 切换回均衡模式
4. [复杂任务]          # 执行复杂任务
```

### 质量优先工作流
```
1. /model premium     # 切换到高质量模式
2. [关键任务]          # 执行关键任务
3. /model auto        # 切换回均衡模式
```

---

*示例更新时间：2026-03-05*