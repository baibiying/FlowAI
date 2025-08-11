import os
import json
from typing import Dict, List, Optional, Tuple
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL')))
        self.account = Account.from_key(os.getenv('PRIVATE_KEY'))
        self.task_contract_address = os.getenv('TASK_CONTRACT_ADDRESS')
        self.dao_contract_address = os.getenv('DAO_CONTRACT_ADDRESS')
        
        # 加载合约ABI
        self.task_contract_abi = self._load_contract_abi('TaskContract')
        self.dao_contract_abi = self._load_contract_abi('DAOContract')
        
        # 初始化合约实例（仅在非测试模式下）
        if self.task_contract_address != '0x0000000000000000000000000000000000000000':
            self.task_contract = self.w3.eth.contract(
                address=self.task_contract_address,
                abi=self.task_contract_abi
            )
            self.dao_contract = self.w3.eth.contract(
                address=self.dao_contract_address,
                abi=self.dao_contract_abi
            )
        else:
            # 测试模式下设置None
            self.task_contract = None
            self.dao_contract = None
    
    def _load_contract_abi(self, contract_name: str) -> List:
        """加载合约ABI"""
        try:
            with open(f'contracts/{contract_name}.json', 'r') as f:
                contract_data = json.load(f)
                return contract_data['abi']
        except FileNotFoundError:
            # 如果ABI文件不存在，返回基本ABI
            return self._get_basic_abi(contract_name)
    
    def _get_basic_abi(self, contract_name: str) -> List:
        """获取基本ABI（用于测试）"""
        if contract_name == 'TaskContract':
            return [
                {
                    "inputs": [{"internalType": "uint256", "name": "taskId", "type": "uint256"}],
                    "name": "claimTask",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [
                        {"internalType": "uint256", "name": "taskId", "type": "uint256"},
                        {"internalType": "string", "name": "result", "type": "string"}
                    ],
                    "name": "completeTask",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"internalType": "uint256", "name": "taskId", "type": "uint256"}],
                    "name": "getTask",
                    "outputs": [
                        {"internalType": "uint256", "name": "id", "type": "uint256"},
                        {"internalType": "address", "name": "publisher", "type": "address"},
                        {"internalType": "string", "name": "title", "type": "string"},
                        {"internalType": "string", "name": "description", "type": "string"},
                        {"internalType": "uint256", "name": "reward", "type": "uint256"},
                        {"internalType": "bool", "name": "isCompleted", "type": "bool"},
                        {"internalType": "bool", "name": "isClaimed", "type": "bool"},
                        {"internalType": "address", "name": "worker", "type": "address"},
                        {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
                        {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                        {"internalType": "string", "name": "taskType", "type": "string"},
                        {"internalType": "string", "name": "requirements", "type": "string"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "getAvailableTasks",
                    "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
        return []
    
    def get_available_tasks(self) -> List[int]:
        """获取可用的任务列表"""
        # 检查是否在测试模式（合约地址为零地址）
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print("🔧 使用测试模式 - 返回模拟任务数据")
            
            # 使用类变量来跟踪已完成的任务和已认领的任务
            if not hasattr(BlockchainClient, '_completed_tasks'):
                BlockchainClient._completed_tasks = set()
            if not hasattr(BlockchainClient, '_claimed_tasks'):
                BlockchainClient._claimed_tasks = set()
            
            # 所有可用任务
            all_tasks = [1, 2, 3, 4, 5]
            
            # 过滤掉已完成和已认领的任务
            available_tasks = [task_id for task_id in all_tasks if task_id not in BlockchainClient._completed_tasks and task_id not in BlockchainClient._claimed_tasks]
            
            print(f"🔧 测试模式 - 当前可用任务: {available_tasks} (已完成: {list(BlockchainClient._completed_tasks)}, 已认领: {list(BlockchainClient._claimed_tasks)})")
            return available_tasks
        
        try:
            tasks = self.task_contract.functions.getAvailableTasks().call()
            return [task_id for task_id in tasks if task_id > 0]
        except Exception as e:
            print(f"获取可用任务失败: {e}")
            return []
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """获取任务详情"""
        # 检查是否在测试模式
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print(f"🔧 使用测试模式 - 返回模拟任务 {task_id} 数据")
            
            # 检查任务是否已完成或已认领
            if not hasattr(BlockchainClient, '_completed_tasks'):
                BlockchainClient._completed_tasks = set()
            if not hasattr(BlockchainClient, '_claimed_tasks'):
                BlockchainClient._claimed_tasks = set()
            
            if task_id in BlockchainClient._completed_tasks:
                print(f"🔧 测试模式 - 任务 {task_id} 已完成，返回None")
                return None  # 已完成的任务返回None
            
            # 注意：已认领的任务仍然可以获取，只是状态会显示为已认领
            # 这样AI Agent可以继续执行已认领的任务
            
            # 返回模拟任务数据
            mock_tasks = {
                1: {
                    'id': 1,
                    'publisher': '0x1234567890123456789012345678901234567890',
                    'title': '编写技术博客文章',
                    'description': '需要一篇关于区块链技术的技术博客文章，字数1000-1500字',
                    'reward': 1000000000000000000,  # 1 ETH
                    'isCompleted': task_id in BlockchainClient._completed_tasks,
                    'isClaimed': task_id in BlockchainClient._claimed_tasks or task_id in BlockchainClient._completed_tasks,
                    'worker': '0x0000000000000000000000000000000000000000' if task_id not in BlockchainClient._claimed_tasks and task_id not in BlockchainClient._completed_tasks else self.get_account_address(),
                    'createdAt': 1640995200,
                    'deadline': 1641081600,
                    'taskType': 'content_writing',
                    'requirements': '技术准确，语言流畅，结构清晰'
                },
                2: {
                    'id': 2,
                    'publisher': '0x2345678901234567890123456789012345678901',
                    'title': '开发智能合约',
                    'description': '开发一个简单的ERC-20代币合约，包含基本的转账功能',
                    'reward': 2000000000000000000,  # 2 ETH
                    'isCompleted': task_id in BlockchainClient._completed_tasks,
                    'isClaimed': task_id in BlockchainClient._claimed_tasks or task_id in BlockchainClient._completed_tasks,
                    'worker': '0x0000000000000000000000000000000000000000' if task_id not in BlockchainClient._claimed_tasks and task_id not in BlockchainClient._completed_tasks else self.get_account_address(),
                    'createdAt': 1640995200,
                    'deadline': 1641168000,
                    'taskType': 'programming',
                    'requirements': '代码规范，注释完整，测试通过'
                },
                3: {
                    'id': 3,
                    'publisher': '0x3456789012345678901234567890123456789012',
                    'title': '设计UI界面',
                    'description': '为DeFi应用设计现代化的用户界面，包含钱包连接功能',
                    'reward': 1500000000000000000,  # 1.5 ETH
                    'isCompleted': task_id in BlockchainClient._completed_tasks,
                    'isClaimed': task_id in BlockchainClient._claimed_tasks or task_id in BlockchainClient._completed_tasks,
                    'worker': '0x0000000000000000000000000000000000000000' if task_id not in BlockchainClient._claimed_tasks and task_id not in BlockchainClient._completed_tasks else self.get_account_address(),
                    'createdAt': 1640995200,
                    'deadline': 1641254400,
                    'taskType': 'design',
                    'requirements': '现代化设计，用户体验良好，响应式布局'
                },
                4: {
                    'id': 4,
                    'publisher': '0x4567890123456789012345678901234567890123',
                    'title': '翻译技术文档',
                    'description': '将英文技术文档翻译成中文，保持专业术语的准确性',
                    'reward': 800000000000000000,  # 0.8 ETH
                    'isCompleted': task_id in BlockchainClient._completed_tasks,
                    'isClaimed': task_id in BlockchainClient._claimed_tasks or task_id in BlockchainClient._completed_tasks,
                    'worker': '0x0000000000000000000000000000000000000000' if task_id not in BlockchainClient._claimed_tasks and task_id not in BlockchainClient._completed_tasks else self.get_account_address(),
                    'createdAt': 1640995200,
                    'deadline': 1641340800,
                    'taskType': 'translation',
                    'requirements': '翻译准确，术语统一，语言流畅'
                },
                5: {
                    'id': 5,
                    'publisher': '0x5678901234567890123456789012345678901234',
                    'title': '市场调研报告',
                    'description': '对DeFi市场进行深入调研，分析当前趋势和机会',
                    'reward': 3000000000000000000,  # 3 ETH
                    'isCompleted': task_id in BlockchainClient._completed_tasks,
                    'isClaimed': task_id in BlockchainClient._claimed_tasks or task_id in BlockchainClient._completed_tasks,
                    'worker': '0x0000000000000000000000000000000000000000' if task_id not in BlockchainClient._claimed_tasks and task_id not in BlockchainClient._completed_tasks else self.get_account_address(),
                    'createdAt': 1640995200,
                    'deadline': 1641427200,
                    'taskType': 'research',
                    'requirements': '数据准确，分析深入，结论有价值'
                }
            }
            return mock_tasks.get(task_id)
        
        try:
            task_data = self.task_contract.functions.getTask(task_id).call()
            return {
                'id': task_data[0],
                'publisher': task_data[1],
                'title': task_data[2],
                'description': task_data[3],
                'reward': task_data[4],
                'isCompleted': task_data[5],
                'isClaimed': task_data[6],
                'worker': task_data[7],
                'createdAt': task_data[8],
                'deadline': task_data[9],
                'taskType': task_data[10],
                'requirements': task_data[11]
            }
        except Exception as e:
            print(f"获取任务详情失败: {e}")
            return None
    
    def claim_task(self, task_id: int) -> bool:
        """认领任务"""
        # 检查是否在测试模式
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print(f"🔧 使用测试模式 - 模拟认领任务 {task_id}")
            
            # 将任务添加到已认领任务集合中
            if not hasattr(BlockchainClient, '_claimed_tasks'):
                BlockchainClient._claimed_tasks = set()
            BlockchainClient._claimed_tasks.add(task_id)
            
            print(f"🔧 测试模式 - 任务 {task_id} 已认领，已从可用任务中移除")
            return True  # 在测试模式下总是成功
        
        try:
            # 构建交易
            transaction = self.task_contract.functions.claimTask(task_id).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # 签名交易
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            
            # 发送交易
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 等待交易确认
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return tx_receipt.status == 1
        except Exception as e:
            print(f"认领任务失败: {e}")
            return False
    
    def complete_task(self, task_id: int, result: str) -> bool:
        """完成任务"""
        # 检查是否在测试模式
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print(f"🔧 使用测试模式 - 模拟完成任务 {task_id}")
            
            # 将任务添加到已完成任务集合中
            if not hasattr(BlockchainClient, '_completed_tasks'):
                BlockchainClient._completed_tasks = set()
            BlockchainClient._completed_tasks.add(task_id)
            
            # 更新工人统计数据
            if not hasattr(BlockchainClient, '_worker_stats'):
                BlockchainClient._worker_stats = {
                    'completed_tasks': 0,
                    'total_earnings': 0,
                    'reputation': 50
                }
            
            # 获取任务信息以计算奖励
            task_info = self.get_task(task_id)
            if task_info:
                reward = task_info.get('reward', 0)
            else:
                # 如果任务信息获取失败，使用模拟数据
                mock_rewards = {1: 1000000000000000000, 2: 2000000000000000000, 3: 1500000000000000000, 4: 800000000000000000, 5: 3000000000000000000}
                reward = mock_rewards.get(task_id, 1000000000000000000)
            
            BlockchainClient._worker_stats['completed_tasks'] += 1
            BlockchainClient._worker_stats['total_earnings'] += reward
            BlockchainClient._worker_stats['reputation'] += 5  # 每完成一个任务增加5点声誉
            
            # 更新余额（增加任务奖励）
            if not hasattr(BlockchainClient, '_balance'):
                BlockchainClient._balance = 0  # 初始0 ETH
            BlockchainClient._balance += reward
            
            print(f"🔧 测试模式 - 任务 {task_id} 已完成")
            print(f"🔧 测试模式 - 更新统计: 完成任务数={BlockchainClient._worker_stats['completed_tasks']}, 总收入={BlockchainClient._worker_stats['total_earnings']}, 声誉={BlockchainClient._worker_stats['reputation']}, 余额={BlockchainClient._balance}")
            
            return True  # 在测试模式下总是成功
        
        try:
            # 构建交易
            transaction = self.task_contract.functions.completeTask(task_id, result).build_transaction({
                'from': self.account.address,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # 签名交易
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            
            # 发送交易
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 等待交易确认
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return tx_receipt.status == 1
        except Exception as e:
            print(f"完成任务失败: {e}")
            return False
    
    def get_worker_info(self, worker_address: str) -> Optional[Dict]:
        """获取工人信息"""
        # 检查是否在测试模式
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print(f"🔧 使用测试模式 - 返回动态工人信息")
            
            # 使用类变量来跟踪统计数据
            if not hasattr(BlockchainClient, '_worker_stats'):
                BlockchainClient._worker_stats = {
                    'completed_tasks': 0,
                    'total_earnings': 0,
                    'reputation': 50  # 初始声誉
                }
            
            print(f"🔧 测试模式 - 当前统计: 完成任务={BlockchainClient._worker_stats['completed_tasks']}, 总收入={BlockchainClient._worker_stats['total_earnings']}, 声誉={BlockchainClient._worker_stats['reputation']}")
            
            return {
                'addr': worker_address,
                'reputation': BlockchainClient._worker_stats['reputation'],
                'completedTasks': BlockchainClient._worker_stats['completed_tasks'],
                'totalEarnings': BlockchainClient._worker_stats['total_earnings'],
                'isActive': True
            }
        
        try:
            worker_data = self.task_contract.functions.getWorker(worker_address).call()
            return {
                'addr': worker_data[0],
                'reputation': worker_data[1],
                'completedTasks': worker_data[2],
                'totalEarnings': worker_data[3],
                'isActive': worker_data[4]
            }
        except Exception as e:
            print(f"获取工人信息失败: {e}")
            return None
    
    def get_worker_tasks(self, worker_address: str) -> List[int]:
        """获取工人的任务列表"""
        try:
            tasks = self.task_contract.functions.getWorkerTasks(worker_address).call()
            return [task_id for task_id in tasks if task_id > 0]
        except Exception as e:
            print(f"获取工人任务失败: {e}")
            return []
    
    def get_balance(self, address: str) -> int:
        """获取账户余额"""
        # 检查是否在测试模式
        if self.task_contract_address == '0x0000000000000000000000000000000000000000':
            print(f"🔧 使用测试模式 - 返回模拟余额")
            
            # 使用类变量来跟踪余额
            if not hasattr(BlockchainClient, '_balance'):
                BlockchainClient._balance = 0  # 初始0 ETH
            
            return BlockchainClient._balance
        
        try:
            return self.w3.eth.get_balance(address)
        except Exception as e:
            print(f"获取余额失败: {e}")
            return 0
    
    def get_account_address(self) -> str:
        """获取当前账户地址"""
        return self.account.address
    
    def is_connected(self) -> bool:
        """检查是否连接到区块链网络"""
        return self.w3.is_connected()
    
    def get_network_info(self) -> Dict:
        """获取网络信息"""
        try:
            return {
                'chain_id': self.w3.eth.chain_id,
                'block_number': self.w3.eth.block_number,
                'gas_price': self.w3.eth.gas_price,
                'is_connected': self.w3.is_connected()
            }
        except Exception as e:
            print(f"获取网络信息失败: {e}")
            return {} 