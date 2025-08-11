import os
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.task_agent import TaskAgent
from blockchain.blockchain_client import BlockchainClient

load_dotenv()

app = FastAPI(
    title="FlowAI - 区块链AI Agent平台",
    description="去中心化的AI工作代理平台",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 初始化组件
task_agent = TaskAgent()
blockchain_client = task_agent.blockchain_client  # 使用TaskAgent的blockchain_client实例

# Pydantic模型
class TaskInfo(BaseModel):
    id: int
    title: str
    description: str
    reward: int
    task_type: str
    requirements: str
    deadline: int
    publisher: str
    is_claimed: bool
    is_completed: bool

class WorkerStats(BaseModel):
    address: str
    reputation: int
    completed_tasks: int
    total_earnings: int
    is_active: bool

class WorkResult(BaseModel):
    status: str
    message: str
    task_id: Optional[int] = None
    task_title: Optional[str] = None
    reward: Optional[int] = None
    result: Optional[str] = None

class NetworkInfo(BaseModel):
    chain_id: int
    block_number: int
    gas_price: int
    is_connected: bool

# API路由
@app.get("/")
async def root():
    """根路径 - 返回Web界面"""
    from fastapi.responses import FileResponse
    return FileResponse("web/index.html")

@app.get("/api")
async def api_root():
    """API根路径"""
    return {
        "message": "FlowAI - 区块链AI Agent平台",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    try:
        network_info = blockchain_client.get_network_info()
        return {
            "status": "healthy",
            "blockchain_connected": network_info.get("is_connected", False),
            "agent_ready": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/api/tasks/available", response_model=List[TaskInfo])
async def get_available_tasks():
    """获取可用任务列表"""
    try:
        available_task_ids = blockchain_client.get_available_tasks()
        tasks = []
        
        for task_id in available_task_ids:
            task_data = blockchain_client.get_task(task_id)
            if task_data:
                task_info = TaskInfo(
                    id=task_data['id'],
                    title=task_data['title'],
                    description=task_data['description'],
                    reward=task_data['reward'],
                    task_type=task_data.get('taskType', 'general'),
                    requirements=task_data.get('requirements', ''),
                    deadline=task_data['deadline'],
                    publisher=task_data['publisher'],
                    is_claimed=task_data['isClaimed'],
                    is_completed=task_data['isCompleted']
                )
                tasks.append(task_info)
        
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")

@app.get("/api/tasks/{task_id}", response_model=TaskInfo)
async def get_task(task_id: int):
    """获取特定任务详情"""
    try:
        task_data = blockchain_client.get_task(task_id)
        if not task_data:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return TaskInfo(
            id=task_data['id'],
            title=task_data['title'],
            description=task_data['description'],
            reward=task_data['reward'],
            task_type=task_data.get('taskType', 'general'),
            requirements=task_data.get('requirements', ''),
            deadline=task_data['deadline'],
            publisher=task_data['publisher'],
            is_claimed=task_data['isClaimed'],
            is_completed=task_data['isCompleted']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务详情失败: {str(e)}")

@app.post("/api/tasks/{task_id}/claim")
async def claim_task(task_id: int):
    """认领任务"""
    try:
        success = blockchain_client.claim_task(task_id)
        if success:
            return {"status": "success", "message": "任务认领成功"}
        else:
            raise HTTPException(status_code=400, detail="任务认领失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"认领任务失败: {str(e)}")

@app.post("/api/tasks/{task_id}/complete")
async def complete_task(task_id: int, result: str):
    """完成任务"""
    try:
        success = blockchain_client.complete_task(task_id, result)
        if success:
            return {"status": "success", "message": "任务完成成功"}
        else:
            raise HTTPException(status_code=400, detail="任务完成失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"完成任务失败: {str(e)}")

@app.get("/api/worker/stats", response_model=WorkerStats)
async def get_worker_stats():
    """获取工人统计信息"""
    try:
        stats = task_agent.get_worker_stats()
        return WorkerStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工人统计失败: {str(e)}")

@app.get("/api/worker/balance")
async def get_worker_balance():
    """获取工人余额"""
    try:
        balance = task_agent.get_balance()
        return {
            "balance_wei": balance,
            "balance_eth": balance / 10**18
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取余额失败: {str(e)}")

@app.post("/api/agent/work", response_model=WorkResult)
async def start_work_cycle(background_tasks: BackgroundTasks):
    """启动AI Agent工作周期"""
    try:
        # 在后台执行工作周期
        background_tasks.add_task(task_agent.work_cycle)
        return {
            "status": "started",
            "message": "AI Agent已开始工作"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动工作周期失败: {str(e)}")

@app.post("/api/agent/work/sync", response_model=WorkResult)
async def work_cycle_sync():
    """同步执行AI Agent工作周期"""
    try:
        result = await task_agent.work_cycle()
        
        # 确保返回的数据符合WorkResult模型
        work_result = {
            "status": result.get("status", "unknown"),
            "message": result.get("message", ""),
            "task_id": result.get("task_id"),
            "task_title": result.get("task_title"),
            "reward": result.get("reward"),
            "result": result.get("result")
        }
        
        return WorkResult(**work_result)
    except Exception as e:
        print(f"工作周期执行失败: {e}")
        raise HTTPException(status_code=500, detail=f"工作周期执行失败: {str(e)}")

@app.get("/api/network/info", response_model=NetworkInfo)
async def get_network_info():
    """获取网络信息"""
    try:
        network_info = blockchain_client.get_network_info()
        return NetworkInfo(**network_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取网络信息失败: {str(e)}")

@app.get("/api/account/address")
async def get_account_address():
    """获取当前账户地址"""
    try:
        address = blockchain_client.get_account_address()
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取账户地址失败: {str(e)}")

# 后台任务
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    print("FlowAI 应用启动中...")
    
    # 检查区块链连接
    if not blockchain_client.is_connected():
        print("警告: 无法连接到区块链网络")
    else:
        print("区块链连接正常")
    
    print("FlowAI 应用启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    print("FlowAI 应用关闭中...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    ) 