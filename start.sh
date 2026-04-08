#!/bin/bash
# zhilinainovel 启动脚本

set -e

# 加载 .env 文件（如果存在）
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 检查 API Key
if [ -z "$OPENAI_API_KEY" ] && [ -z "$MINIMAX_API_KEY" ]; then
    echo "⚠️  未设置 API Key，请先配置 .env 文件"
    echo ""
    echo "步骤："
    echo "  1. cp .env.example .env"
    echo "  2. 编辑 .env，填入你的 API Key"
    echo "  3. 重新运行此脚本"
    echo ""
    echo "快速启动 Streamlit："
    echo "  streamlit run web_app.py"
    echo ""
    echo "快速启动 API 服务器："
    echo "  python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080"
    exit 1
fi

echo "✅ 环境变量检查通过"
echo "   模型: ${MODEL:-MiniMax-M2.5}"
echo "   基础URL: ${OPENAI_BASE_URL:-https://api.minimax.chat/v1}"
echo ""

# 解析命令行参数
MODE=${1:-api}

if [ "$MODE" = "api" ]; then
    echo "🚀 启动 API 服务器..."
    python -m uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8080} --reload

elif [ "$MODE" = "web" ]; then
    echo "🚀 启动 Streamlit Web UI..."
    streamlit run web_app.py --server.port 8501 --browser.gatherUsageStats=false

elif [ "$MODE" = "both" ]; then
    echo "🚀 同时启动 API + Web UI..."
    python -m uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8080} &
    sleep 2
    streamlit run web_app.py --server.port 8501 --browser.gatherUsageStats=false

else
    echo "未知模式: $MODE"
    echo "用法: ./start.sh [api|web|both]"
fi
