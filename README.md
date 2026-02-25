# zhilinainovel

使用 AI 创作各种题材小说的项目

## 项目目标

- 学习使用 AI 辅助小说创作
- 掌握不同题材小说的写作技巧
- 完成后可通过 Docker 部署

## 项目周期

一周（7天）

## 技术栈

- Python 3.11+
- OpenAI API / MiniMax API
- Flask/FastAPI (可选)
- Docker

## 目录结构

```
zhilinainovel/
├── src/              # 源代码
├── prompts/          # 提示词模板
├── templates/        # 小说模板
├── docker/           # Docker配置
└── README.md
```

## 学习内容

### Day 1-2: 基础入门
- AI 写作原理
- 提示词工程基础
- 安装配置开发环境

### Day 3-4: 题材探索
- 玄幻/奇幻
- 都市/言情
- 悬疑/推理
- 科幻

### Day 5-6: 实战创作
- 人物塑造
- 情节设计
- 对话生成

### Day 7: 部署上线
- Docker 容器化
- 部署配置
- 测试优化

## 使用方法

```bash
# 本地运行
python src/main.py

# Docker 部署
docker build -t zhilinainovel .
docker run -p 8080:8080 zhilinainovel
```

## 注意事项

- 需要配置 API Key
- 遵守相关平台使用规范
