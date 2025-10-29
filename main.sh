#!/bin/bash

# AI-Trader 主启动脚本
# 用于启动完整的加密货币交易环境

set -e  # 遇到错误时退出

echo "🚀 启动 AI Trader 加密货币交易环境..."

echo "🔧 启动 MCP 服务..."
cd ./agent_tools
python start_mcp_services.py &
MCP_PID=$!
cd ../

# 等待 MCP 服务启动
echo "⏳ 等待 MCP 服务启动..."
sleep 5

echo "🤖 启动主交易代理..."
python main.py configs/okx_crypto_config.json

echo "✅ AI-Trader 已停止"

# 清理后台进程
kill $MCP_PID 2>/dev/null || true

echo "🔄 启动 Web 服务器..."
cd ./docs
python3 -m http.server 8888

echo "✅ Web 服务器已启动"