# MiniMax API 配置

## 模型选择

### Coding Plus 套餐推荐模型

| 场景 | 推荐模型 | 说明 |
|------|----------|------|
| 代码生成 | `Moonshot AI - kimi-code` | 专为代码优化 |
| 通用对话 | `MiniMax-M2.5` | 性价比最高 |
| 长文本 | `MiniMax-Text-01` | 200K上下文 |
| 快速推理 | `MiniMax-Reasoning` | 低延迟 |

## API 配置

```bash
# 环境变量
OPENAI_API_KEY=你的APIKey
OPENAI_BASE_URL=https://api.minimax.chat/v1

# 可用模型列表
- Moonshot AI: kimi-code, kimi-for-codi
- MiniMax: MiniMax-M2.5, MiniMax-Text-01, MiniMax-Reasoning
```

## 项目应用场景

### 1. 代码开发
- 自动补全代码
- Bug修复
- 代码重构

### 2. 内容创作
- 小说生成（zhilinainovel核心能力）
- 长文写作
- 脚本生成

### 3. 知识处理
- 文档摘要
- 知识提取
- 基因分析

## 优化建议

1. **批量处理** - 积累多条任务一起请求，降低API调用开销
2. **缓存复用** - 相同请求缓存结果
3. **流式输出** - 长文本用streaming减少等待
4. **上下文复用** - 保持对话上下文减少token
