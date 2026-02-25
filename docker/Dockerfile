FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制代码
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY templates/ ./templates/

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "src/main.py"]
