#!/bin/bash

# FlowAI 快速启动脚本

echo "🚀 FlowAI - 区块链AI Agent平台"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
    echo "✅ Python版本: $(python3 --version)"
else
    echo "❌ 需要Python 3.8或更高版本"
    exit 1
fi

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 建议使用虚拟环境"
    echo "   创建虚拟环境: python3 -m venv venv"
    echo "   激活虚拟环境: source venv/bin/activate"
fi

# 检查依赖
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ 未找到requirements.txt文件"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 检查环境变量
if [[ ! -f ".env" ]]; then
    if [[ -f "env_example.txt" ]]; then
        echo "🔧 创建环境变量文件..."
        cp env_example.txt .env
        echo "⚠️  请编辑 .env 文件并填入必要的配置"
        echo "   特别是: OPENAI_API_KEY, ETHEREUM_RPC_URL, PRIVATE_KEY"
    else
        echo "❌ 未找到环境变量模板文件"
        exit 1
    fi
fi

# 检查启动参数
if [[ $# -eq 0 ]]; then
    echo ""
    echo "使用方法:"
    echo "  ./start.sh web     # 启动Web界面"
    echo "  ./start.sh agent   # 启动AI Agent"
    echo "  ./start.sh full    # 启动完整服务"
    echo "  ./start.sh test    # 运行测试"
    echo ""
    echo "默认启动Web界面..."
    python3 main.py web
else
    case $1 in
        "web")
            echo "🌐 启动Web界面..."
            python3 main.py web
            ;;
        "agent")
            echo "🤖 启动AI Agent..."
            python3 main.py agent
            ;;
        "full")
            echo "🚀 启动完整服务..."
            python3 main.py full
            ;;
        "test")
            echo "🧪 运行测试..."
            python3 main.py test
            ;;
        "deploy")
            echo "🔧 运行部署脚本..."
            python3 deploy.py
            ;;
        *)
            echo "❌ 未知命令: $1"
            echo "可用命令: web, agent, full, test, deploy"
            exit 1
            ;;
    esac
fi 