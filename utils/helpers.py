"""
FlowAI 工具函数
提供各种辅助功能
"""

import os
import json
import hashlib
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from web3 import Web3

def format_eth_amount(wei_amount: int, decimals: int = 4) -> str:
    """格式化ETH金额显示"""
    eth_amount = wei_amount / 10**18
    return f"{eth_amount:.{decimals}f} ETH"

def format_wei_amount(wei_amount: int) -> str:
    """格式化Wei金额显示"""
    return f"{wei_amount} Wei"

def format_address(address: str, length: int = 8) -> str:
    """格式化地址显示"""
    if not address or address == "0x0000000000000000000000000000000000000000":
        return "未设置"
    return f"{address[:length]}...{address[-length:]}"

def format_timestamp(timestamp: int) -> str:
    """格式化时间戳"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_task_score(task: Dict[str, Any]) -> float:
    """计算任务评分"""
    score = 0
    
    # 基础分数
    score += 10
    
    # 奖励分数
    reward_eth = task.get('reward', 0) / 10**18
    score += reward_eth * 100
    
    # 时间紧迫性
    deadline = task.get('deadline', 0)
    current_time = int(time.time())
    time_left = deadline - current_time
    
    if time_left > 86400:  # 超过1天
        score += 5
    elif time_left > 3600:  # 超过1小时
        score += 10
    else:  # 紧急任务
        score += 15
    
    # 任务类型偏好
    task_type = task.get('taskType', '').lower()
    if 'content' in task_type or 'writing' in task_type:
        score += 20
    elif 'programming' in task_type or 'code' in task_type:
        score += 15
    elif 'research' in task_type:
        score += 10
    
    return score

def validate_ethereum_address(address: str) -> bool:
    """验证以太坊地址格式"""
    if not address:
        return False
    
    # 检查长度
    if len(address) != 42:
        return False
    
    # 检查前缀
    if not address.startswith('0x'):
        return False
    
    # 检查字符
    try:
        int(address[2:], 16)
    except ValueError:
        return False
    
    return True

def generate_task_hash(task_data: Dict[str, Any]) -> str:
    """生成任务哈希"""
    # 创建任务数据的字符串表示
    task_string = json.dumps(task_data, sort_keys=True)
    return hashlib.sha256(task_string.encode()).hexdigest()

def estimate_gas_price(network_info: Dict[str, Any]) -> int:
    """估算Gas价格"""
    base_gas_price = network_info.get('gas_price', 20000000000)  # 20 Gwei
    
    # 根据网络拥堵情况调整
    block_number = network_info.get('block_number', 0)
    # 简单的拥堵检测（实际应用中需要更复杂的逻辑）
    if block_number % 100 == 0:
        return int(base_gas_price * 1.2)  # 增加20%
    
    return base_gas_price

def calculate_reward_ratio(task_reward: int, gas_cost: int) -> float:
    """计算奖励与成本比率"""
    if gas_cost == 0:
        return float('inf')
    
    return task_reward / gas_cost

def is_task_profitable(task_reward: int, estimated_gas: int, gas_price: int) -> bool:
    """判断任务是否有利可图"""
    gas_cost = estimated_gas * gas_price
    reward_ratio = calculate_reward_ratio(task_reward, gas_cost)
    
    # 如果奖励是成本的至少2倍，认为有利可图
    return reward_ratio >= 2.0

def format_duration(seconds: int) -> str:
    """格式化持续时间"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}分钟"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}小时"
    else:
        days = seconds // 86400
        return f"{days}天"

def get_task_difficulty(task_description: str) -> str:
    """评估任务难度"""
    description_lower = task_description.lower()
    
    # 简单关键词匹配
    easy_keywords = ['简单', '基础', '入门', 'easy', 'basic', 'simple']
    hard_keywords = ['复杂', '高级', '专家', 'difficult', 'advanced', 'expert', 'complex']
    
    if any(keyword in description_lower for keyword in easy_keywords):
        return 'easy'
    elif any(keyword in description_lower for keyword in hard_keywords):
        return 'hard'
    else:
        return 'medium'

def estimate_task_duration(task_type: str, task_description: str) -> str:
    """估算任务完成时间"""
    difficulty = get_task_difficulty(task_description)
    
    # 基于任务类型和难度的估算
    base_times = {
        'content_writing': {'easy': 30, 'medium': 60, 'hard': 120},
        'programming': {'easy': 60, 'medium': 120, 'hard': 240},
        'design': {'easy': 45, 'medium': 90, 'hard': 180},
        'translation': {'easy': 20, 'medium': 40, 'hard': 80},
        'research': {'easy': 60, 'medium': 120, 'hard': 240}
    }
    
    task_type_lower = task_type.lower()
    for key, times in base_times.items():
        if key in task_type_lower:
            minutes = times.get(difficulty, 60)
            return format_duration(minutes * 60)
    
    # 默认估算
    default_times = {'easy': 30, 'medium': 60, 'hard': 120}
    minutes = default_times.get(difficulty, 60)
    return format_duration(minutes * 60)

def create_task_summary(task: Dict[str, Any]) -> Dict[str, Any]:
    """创建任务摘要"""
    return {
        'id': task.get('id'),
        'title': task.get('title'),
        'reward_eth': format_eth_amount(task.get('reward', 0)),
        'task_type': task.get('taskType', 'general'),
        'difficulty': get_task_difficulty(task.get('description', '')),
        'estimated_duration': estimate_task_duration(
            task.get('taskType', 'general'),
            task.get('description', '')
        ),
        'deadline': format_timestamp(task.get('deadline', 0)),
        'publisher': format_address(task.get('publisher', '')),
        'score': calculate_task_score(task)
    }

def log_activity(activity_type: str, details: Dict[str, Any]) -> None:
    """记录活动日志"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'type': activity_type,
        'details': details
    }
    
    # 这里可以集成到日志系统
    print(f"[{timestamp}] {activity_type}: {details}")

def validate_environment() -> Dict[str, bool]:
    """验证环境配置"""
    results = {
        'openai_api_key': bool(os.getenv('OPENAI_API_KEY')),
        'ethereum_rpc_url': bool(os.getenv('ETHEREUM_RPC_URL')),
        'private_key': bool(os.getenv('PRIVATE_KEY')),
        'task_contract': bool(os.getenv('TASK_CONTRACT_ADDRESS')),
        'dao_contract': bool(os.getenv('DAO_CONTRACT_ADDRESS'))
    }
    
    return results

def get_system_status() -> Dict[str, Any]:
    """获取系统状态"""
    env_status = validate_environment()
    
    return {
        'environment': env_status,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    } 