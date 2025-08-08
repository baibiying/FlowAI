#!/usr/bin/env python3
"""
FlowAI - 区块链AI Agent平台
去中心化的AI工作代理平台

作者: FlowAI Team
版本: 1.0.0
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv()

def check_dependencies():
    """检查必要的依赖和环境变量"""
    required_env_vars = [
        'OPENAI_API_KEY',
        'ETHEREUM_RPC_URL',
        'PRIVATE_KEY'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请复制 env_example.txt 为 .env 并填入相应的值")
        return False
    
    return True

def check_contract_addresses():
    """检查智能合约地址配置"""
    task_contract = os.getenv('TASK_CONTRACT_ADDRESS')
    dao_contract = os.getenv('DAO_CONTRACT_ADDRESS')
    
    if task_contract == '0x0000000000000000000000000000000000000000':
        print("⚠️  警告: TASK_CONTRACT_ADDRESS 未配置，将使用测试模式")
    
    if dao_contract == '0x0000000000000000000000000000000000000000':
        print("⚠️  警告: DAO_CONTRACT_ADDRESS 未配置，将使用测试模式")
    
    return True

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🤖 FlowAI Platform 🤖                    ║
    ║                                                              ║
    ║        区块链AI Agent平台 - 去中心化的打工人模式              ║
    ║                                                              ║
    ║    让AI Agent在区块链上自动认领任务、执行工作、获得报酬       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_usage():
    """打印使用说明"""
    usage = """
    使用方法:
    
    1. 启动Web界面:
       python main.py web
    
    2. 启动AI Agent工作模式:
       python main.py agent
    
    3. 启动完整服务:
       python main.py full
    
    4. 运行测试:
       python main.py test
    
    5. 显示帮助:
       python main.py help
    """
    print(usage)

async def start_web_server():
    """启动Web服务器"""
    try:
        import uvicorn
        
        print("🌐 启动Web服务器...")
        uvicorn.run(
            "api.main:app",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", 8000)),
            reload=True
        )
    except Exception as e:
        print(f"❌ Web服务器启动失败: {e}")

async def start_agent_worker():
    """启动AI Agent工作模式"""
    try:
        from agents.task_agent import TaskAgent
        
        print("🤖 启动AI Agent工作模式...")
        agent = TaskAgent()
        
        print("✅ AI Agent已启动，开始自动工作...")
        print("按 Ctrl+C 停止工作")
        
        while True:
            try:
                result = await agent.work_cycle()
                print(f"📊 工作结果: {result}")
                
                if result['status'] == 'success':
                    print(f"🎉 任务完成！获得 {result['reward'] / 1e18:.4f} ETH")
                elif result['status'] == 'no_tasks':
                    print("⏳ 当前没有可用任务，等待中...")
                else:
                    print(f"ℹ️  {result['message']}")
                
                # 等待一段时间再继续
                await asyncio.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🛑 用户中断，停止工作")
                break
            except Exception as e:
                print(f"❌ 工作周期出错: {e}")
                await asyncio.sleep(10)
                
    except Exception as e:
        print(f"❌ AI Agent启动失败: {e}")

async def start_full_service():
    """启动完整服务（Web + Agent）"""
    print("🚀 启动完整服务...")
    
    # 启动AI Agent后台任务
    agent_task = asyncio.create_task(start_agent_worker())
    
    # 启动Web服务器
    web_task = asyncio.create_task(start_web_server())
    
    try:
        await asyncio.gather(agent_task, web_task)
    except KeyboardInterrupt:
        print("\n🛑 服务停止")
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    
    try:
        # 测试区块链连接
        from blockchain.blockchain_client import BlockchainClient
        client = BlockchainClient()
        
        if client.is_connected():
            print("✅ 区块链连接正常")
        else:
            print("❌ 区块链连接失败")
        
        # 测试AI Agent
        from agents.task_agent import TaskAgent
        agent = TaskAgent()
        print("✅ AI Agent初始化成功")
        
        # 测试网络信息
        network_info = client.get_network_info()
        print(f"📊 网络信息: {network_info}")
        
        print("✅ 所有测试通过")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查合约地址
    check_contract_addresses()
    
    # 解析命令行参数
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "web":
        asyncio.run(start_web_server())
    elif command == "agent":
        asyncio.run(start_agent_worker())
    elif command == "full":
        asyncio.run(start_full_service())
    elif command == "test":
        run_tests()
    elif command == "help":
        print_usage()
    else:
        print(f"❌ 未知命令: {command}")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main() 