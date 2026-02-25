# zhilinainovel

> AI 小说创作助手 - 智能分析 · 风格克隆 · 自动化创作

## 🎯 项目目标

1. **定期搜索** - 自动采集各类小说排行榜数据
2. **分析优秀基因** - 解析热门小说的成功要素（人设、节奏、金句、爽点）
3. **风格克隆** - 学习不同题材的写作风格，形成可复用的基因库
4. **辅助创作** - 为用户提供创作灵感、素材、金句

## 📅 项目周期

一周（7天）

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    zhilinainovel                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  数据采集层  │  │  分析引擎    │  │  创作引擎    │   │
│  │             │  │             │  │             │   │
│  │ 排行榜抓取   │  │ 风格基因提取  │  │ 素材生成     │   │
│  │ 内容解析     │  │ 爽点分析     │  │ 对话生成     │   │
│  │ 章节入库     │  │ 人设拆解     │  │ 情节构建     │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├─────────────────────────────────────────────────────────┤
│                      基因库 (SQLite)                      │
│  ├── 题材基因（玄幻/都市/悬疑/科幻...）                    │
│  ├── 风格基因（文笔/节奏/情绪曲线）                        │
│  ├── 爽点基因（打脸/逆袭/甜宠...）                        │
│  └── 金句库                                               │
└─────────────────────────────────────────────────────────┘
```

## 📂 目录结构

```
zhilinainovel/
├── src/
│   ├── crawler/          # 数据采集
│   │   ├── ranking.py    # 排行榜抓取
│   │   └── parser.py     # 内容解析
│   ├── analyzer/         # 分析引擎
│   │   ├── gene.py       # 基因提取
│   │   ├── sentiment.py  # 情绪分析
│   │   └── plot.py       # 情节分析
│   ├── generator/        # 创作引擎
│   │   ├── story.py      # 故事生成
│   │   ├── dialogue.py   # 对话生成
│   │   └── outline.py    # 大纲生成
│   ├── database/         # 基因库
│   │   └── db.py
│   ├── scheduler/        # 定时任务
│   │   └── cron.py
│   └── api/              # API服务
│       └── main.py
├── prompts/              # 提示词模板
│   ├── analyze.md
│   ├── generate.md
│   └── gene.md
├── templates/             # 小说模板
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── README.md
```

## 🛠️ 技术栈

- **Python 3.11+**
- **API**: OpenAI / MiniMax
- **数据库**: SQLite（本地基因库）
- **Web**: FastAPI
- **定时任务**: APScheduler
- **数据采集**: requests + BeautifulSoup
- **Docker**

## 📦 功能模块

### 1. 数据采集模块
- [ ] 起点中文网排行榜
- [ ] 番茄小说排行榜
- [ ] 七猫小说排行榜
- [ ] 章节内容解析

### 2. 分析引擎
- [ ] 题材识别
- [ ] 人设提取（主角/配角性格）
- [ ] 爽点分析（打脸/逆袭/甜宠/悬疑...）
- [ ] 情绪曲线分析
- [ ] 金句提取

### 3. 风格基因库
- [ ] 玄幻基因：升级体系、功法设定、世界观
- [ ] 都市基因：职场、豪门、甜宠
- [ ] 悬疑基因：线索埋设、氛围营造
- [ ] 科幻基因：设定严谨、想象力

### 4. 创作引擎
- [ ] 大纲生成
- [ ] 章节续写
- [ ] 对话润色
- [ ] 素材推荐

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/dingzhilin1990/zhilinainovel.git
cd zhilinainovel

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Key

# 4. 启动服务
python src/api/main.py

# 5. Docker 部署
docker-compose up -d
```

## ⚙️ 环境变量

```bash
# .env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.minimax.chat/v1
MODEL=MiniMax-M2.5

# 可选配置
DATABASE_PATH=./data/genes.db
LOG_LEVEL=INFO
```

## 📡 API 接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/analyze` | POST | 分析小说内容，提取基因 |
| `/api/generate/story` | POST | 生成故事大纲 |
| `/api/generate/chapter` | POST | 续写章节 |
| `/api/genes` | GET | 获取基因库 |
| `/api/genes/:type` | GET | 获取特定类型基因 |

## 🌐 EvoMap 集成

> EvoMap 是 AI Agent 协作进化市场，可发布/获取基因胶囊、赚积分

### 功能
- 🧬 **发布基因** - 将分析出的优质基因发布到市场
- 📥 **获取基因** - 从市场获取其他作者的优质基因
- 💰 **赚取积分** - 基因被复用可获得积分奖励
- 🔥 **领取赏金** - 完成写作相关任务获得奖励

### 使用

```python
from src.evomap.client import EvoMapClient, create_novel_gene, create_novel_capsule

# 初始化（自动注册，获得500积分）
client = EvoMapClient()

# 发布小说基因
gene = create_novel_gene("都市", ["职场", "甜宠"], "生活流")
capsule = create_novel_capsule("都市", "请写一个都市爱情故事...")
result = client.publish_bundle(gene, capsule, evolution_event)

# 获取优质基因
assets = client.fetch_assets("Capsule", 10)
```

### 配置

```bash
# .env 添加
EVOMAP_ENABLED=true
```

## 📅 一周开发计划

### Day 1: 基础架构
- [ ] 项目初始化
- [ ] 数据库设计
- [ ] API 框架搭建

### Day 2: 数据采集
- [ ] 排行榜爬虫
- [ ] 内容解析器
- [ ] 数据入库

### Day 3: 分析引擎
- [ ] 提示词设计
- [ ] 基因提取逻辑
- [ ] 测试分析功能

### Day 4: 基因库建设
- [ ] 题材基因模板
- [ ] 风格基因模板
- [ ] 爽点基因模板

### Day 5: 创作引擎
- [ ] 大纲生成
- [ ] 章节续写
- [ ] 对话生成

### Day 6: 定时任务
- [ ] 排行榜自动更新
- [ ] 基因自动学习
- [ ] 定时任务配置

### Day 7: 部署上线
- [ ] Docker 优化
- [ ] 性能测试
- [ ] 部署上线

## 🔐 安全注意

- API Key 需妥善保管，切勿提交到仓库
- 爬虫需遵守目标网站 robots.txt
- 尊重版权，仅供学习交流使用
