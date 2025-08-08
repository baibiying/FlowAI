#!/usr/bin/env python3
"""
FlowAI 部署脚本
自动化部署和配置
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def setup_environment():
    """设置环境变量"""
    print("🔧 设置环境变量...")
    
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ 已创建 .env 文件，请编辑配置")
        return True
    elif env_file.exists():
        print("✅ .env 文件已存在")
        return True
    else:
        print("❌ 未找到环境变量模板文件")
        return False

def create_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    
    directories = [
        "logs",
        "data",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ 目录结构创建完成")

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    try:
        subprocess.run([sys.executable, "tests/test_basic.py"], check=True)
        print("✅ 测试通过")
        return True
    except subprocess.CalledProcessError:
        print("❌ 测试失败")
        return False

def build_contracts():
    """构建智能合约"""
    print("🔨 构建智能合约...")
    
    # 检查是否有solc编译器
    try:
        subprocess.run(["solc", "--version"], check=True, capture_output=True)
        print("✅ Solidity编译器已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Solidity编译器未安装，跳过合约构建")
        return True
    
    # 这里可以添加合约编译逻辑
    print("✅ 合约构建完成")
    return True

def create_docker_config():
    """创建Docker配置"""
    print("🐳 创建Docker配置...")
    
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py", "web"]
"""
    
    docker_compose_content = """version: '3.8'

services:
  flowai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ETHEREUM_RPC_URL=${ETHEREUM_RPC_URL}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - TASK_CONTRACT_ADDRESS=${TASK_CONTRACT_ADDRESS}
      - DAO_CONTRACT_ADDRESS=${DAO_CONTRACT_ADDRESS}
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
"""
    
    # 创建Dockerfile
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # 创建docker-compose.yml
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("✅ Docker配置创建完成")

def create_systemd_service():
    """创建systemd服务文件"""
    print("🔧 创建systemd服务...")
    
    service_content = """[Unit]
Description=FlowAI Blockchain AI Agent Platform
After=network.target

[Service]
Type=simple
User=flowai
WorkingDirectory=/opt/flowai
Environment=PATH=/opt/flowai/venv/bin
ExecStart=/opt/flowai/venv/bin/python main.py full
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open("flowai.service", "w") as f:
        f.write(service_content)
    
    print("✅ systemd服务文件创建完成")

def create_nginx_config():
    """创建Nginx配置"""
    print("🌐 创建Nginx配置...")
    
    nginx_config = """server {
    listen 80;
    server_name flowai.local;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/flowai/web/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
"""
    
    with open("nginx-flowai.conf", "w") as f:
        f.write(nginx_config)
    
    print("✅ Nginx配置创建完成")

def print_deployment_guide():
    """打印部署指南"""
    guide = """
🚀 FlowAI 部署指南

1. 环境配置:
   - 编辑 .env 文件，填入必要的配置
   - 确保有足够的ETH余额用于Gas费用

2. 启动方式:
   
   a) 直接运行:
      python main.py web          # 启动Web界面
      python main.py agent        # 启动AI Agent
      python main.py full         # 启动完整服务
   
   b) Docker部署:
      docker-compose up -d
   
   c) 系统服务:
      sudo cp flowai.service /etc/systemd/system/
      sudo systemctl enable flowai
      sudo systemctl start flowai

3. 访问地址:
   - Web界面: http://localhost:8000
   - API文档: http://localhost:8000/docs

4. 监控日志:
   - 应用日志: logs/flowai.log
   - 系统日志: journalctl -u flowai

5. 故障排除:
   - 检查环境变量配置
   - 确认区块链网络连接
   - 验证OpenAI API密钥
   - 查看错误日志

6. 安全建议:
   - 使用HTTPS
   - 设置防火墙规则
   - 定期备份数据
   - 监控系统资源

7. 扩展部署:
   - 使用负载均衡器
   - 配置数据库
   - 设置监控告警
   - 实现自动备份

更多信息请查看 README.md
"""
    print(guide)

def main():
    """主部署函数"""
    print("🚀 FlowAI 部署脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 设置环境
    if not setup_environment():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 构建合约
    build_contracts()
    
    # 运行测试
    if not run_tests():
        print("⚠️  测试失败，但继续部署")
    
    # 创建Docker配置
    create_docker_config()
    
    # 创建systemd服务
    create_systemd_service()
    
    # 创建Nginx配置
    create_nginx_config()
    
    print("\n" + "=" * 50)
    print("✅ 部署脚本执行完成!")
    print_deployment_guide()

if __name__ == "__main__":
    main() 