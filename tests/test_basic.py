"""
FlowAI 基本测试
测试核心功能模块
"""

import unittest
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.helpers import (
    format_eth_amount,
    format_address,
    validate_ethereum_address,
    calculate_task_score,
    get_task_difficulty,
    estimate_task_duration
)

class TestHelpers(unittest.TestCase):
    """测试工具函数"""
    
    def test_format_eth_amount(self):
        """测试ETH金额格式化"""
        # 测试1 ETH
        self.assertEqual(format_eth_amount(10**18), "1.0000 ETH")
        
        # 测试0.001 ETH
        self.assertEqual(format_eth_amount(10**15), "0.0010 ETH")
        
        # 测试0 ETH
        self.assertEqual(format_eth_amount(0), "0.0000 ETH")
    
    def test_format_address(self):
        """测试地址格式化"""
        test_address = "0x1234567890abcdef1234567890abcdef12345678"
        
        # 测试正常地址
        formatted = format_address(test_address)
        self.assertEqual(formatted, "0x123456...12345678")
        
        # 测试空地址
        self.assertEqual(format_address(""), "未设置")
        
        # 测试零地址
        zero_address = "0x0000000000000000000000000000000000000000"
        self.assertEqual(format_address(zero_address), "未设置")
    
    def test_validate_ethereum_address(self):
        """测试以太坊地址验证"""
        # 有效地址
        valid_address = "0x1234567890abcdef1234567890abcdef12345678"
        self.assertTrue(validate_ethereum_address(valid_address))
        
        # 无效地址
        invalid_addresses = [
            "",  # 空地址
            "0x123",  # 太短
            "1234567890abcdef1234567890abcdef12345678",  # 缺少0x前缀
            "0x1234567890abcdef1234567890abcdef1234567g",  # 无效字符
            "0x1234567890abcdef1234567890abcdef123456789",  # 太长
        ]
        
        for address in invalid_addresses:
            self.assertFalse(validate_ethereum_address(address))
    
    def test_calculate_task_score(self):
        """测试任务评分计算"""
        # 基础任务
        basic_task = {
            'reward': 10**18,  # 1 ETH
            'deadline': int(os.time()) + 3600,  # 1小时后
            'taskType': 'content_writing'
        }
        
        score = calculate_task_score(basic_task)
        self.assertGreater(score, 0)
        
        # 高奖励任务
        high_reward_task = {
            'reward': 5 * 10**18,  # 5 ETH
            'deadline': int(os.time()) + 7200,  # 2小时后
            'taskType': 'programming'
        }
        
        high_score = calculate_task_score(high_reward_task)
        self.assertGreater(high_score, score)
    
    def test_get_task_difficulty(self):
        """测试任务难度评估"""
        # 简单任务
        easy_task = "这是一个简单的入门级任务"
        self.assertEqual(get_task_difficulty(easy_task), 'easy')
        
        # 困难任务
        hard_task = "这是一个复杂的专家级任务"
        self.assertEqual(get_task_difficulty(hard_task), 'hard')
        
        # 中等任务
        medium_task = "这是一个普通任务"
        self.assertEqual(get_task_difficulty(medium_task), 'medium')
    
    def test_estimate_task_duration(self):
        """测试任务时间估算"""
        # 内容写作任务
        content_task = "content_writing"
        content_description = "写一篇简单的文章"
        duration = estimate_task_duration(content_task, content_description)
        self.assertIn("分钟", duration)
        
        # 编程任务
        programming_task = "programming"
        programming_description = "编写一个复杂的算法"
        duration = estimate_task_duration(programming_task, programming_description)
        self.assertIn("分钟", duration)

class TestBlockchainClient(unittest.TestCase):
    """测试区块链客户端"""
    
    def setUp(self):
        """设置测试环境"""
        # 这里可以设置测试用的环境变量
        pass
    
    def test_client_initialization(self):
        """测试客户端初始化"""
        try:
            from blockchain.blockchain_client import BlockchainClient
            client = BlockchainClient()
            # 如果初始化成功，说明基本结构正确
            self.assertTrue(True)
        except Exception as e:
            # 如果环境变量未设置，这是预期的
            self.assertIn("environment", str(e).lower())

class TestTaskAgent(unittest.TestCase):
    """测试任务代理"""
    
    def test_agent_initialization(self):
        """测试代理初始化"""
        try:
            from agents.task_agent import TaskAgent
            agent = TaskAgent()
            # 如果初始化成功，说明基本结构正确
            self.assertTrue(True)
        except Exception as e:
            # 如果环境变量未设置，这是预期的
            self.assertIn("environment", str(e).lower())

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestHelpers))
    test_suite.addTest(unittest.makeSuite(TestBlockchainClient))
    test_suite.addTest(unittest.makeSuite(TestTaskAgent))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ 所有测试通过!")
    else:
        print("\n❌ 部分测试失败!")
        sys.exit(1) 