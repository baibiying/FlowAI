import os
import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from blockchain.blockchain_client import BlockchainClient

load_dotenv()

class TaskAnalysisTool(BaseTool):
    name = "task_analysis"
    description = "分析任务内容，确定任务类型和所需技能"
    
    def _run(self, task_description: str) -> str:
        """分析任务内容"""
        analysis = {
            "task_type": "unknown",
            "required_skills": [],
            "estimated_difficulty": "medium",
            "estimated_time": "1-2 hours"
        }
        
        # 简单的任务类型识别
        description_lower = task_description.lower()
        
        if any(word in description_lower for word in ["write", "content", "article", "blog"]):
            analysis["task_type"] = "content_writing"
            analysis["required_skills"] = ["writing", "research", "creativity"]
        elif any(word in description_lower for word in ["code", "program", "develop", "software"]):
            analysis["task_type"] = "programming"
            analysis["required_skills"] = ["coding", "problem_solving", "technical"]
        elif any(word in description_lower for word in ["design", "graphic", "visual", "ui"]):
            analysis["task_type"] = "design"
            analysis["required_skills"] = ["design", "creativity", "visual"]
        elif any(word in description_lower for word in ["translate", "language", "translation"]):
            analysis["task_type"] = "translation"
            analysis["required_skills"] = ["language", "translation"]
        elif any(word in description_lower for word in ["research", "analysis", "data"]):
            analysis["task_type"] = "research"
            analysis["required_skills"] = ["research", "analysis", "data_processing"]
        
        return json.dumps(analysis, ensure_ascii=False)

class TaskExecutionTool(BaseTool):
    name = "task_execution"
    description = "执行具体任务并生成结果"
    
    def __init__(self):
        super().__init__()
    
    def _run(self, task_info: str) -> str:
        """执行任务"""
        try:
            task_data = json.loads(task_info)
            task_type = task_data.get("task_type", "unknown")
            task_description = task_data.get("description", "")
            requirements = task_data.get("requirements", "")
            
            # 创建LLM实例
            llm = ChatOpenAI(
                model="deepseek-v3-250324",
                temperature=0.7,
                api_key=os.getenv('OPENAI_API_KEY'),
                openai_api_base="https://ark.cn-beijing.volces.com/api/v3"
            )
            
            # 根据任务类型生成执行策略
            if task_type == "content_writing":
                return self._execute_content_writing(task_description, requirements, llm)
            elif task_type == "programming":
                return self._execute_programming(task_description, requirements, llm)
            elif task_type == "design":
                return self._execute_design(task_description, requirements, llm)
            elif task_type == "translation":
                return self._execute_translation(task_description, requirements, llm)
            elif task_type == "research":
                return self._execute_research(task_description, requirements, llm)
            else:
                return self._execute_general_task(task_description, requirements, llm)
                
        except Exception as e:
            return f"任务执行失败: {str(e)}"
    
    def _execute_content_writing(self, description: str, requirements: str, llm) -> str:
        """执行内容写作任务"""
        prompt = f"""
        请根据以下要求创作内容：
        
        任务描述：{description}
        具体要求：{requirements}
        
        请创作一篇高质量的内容，确保：
        1. 内容原创且有价值
        2. 符合要求的技术规范
        3. 结构清晰，逻辑合理
        4. 语言流畅，表达准确
        
        请直接输出创作的内容：
        """
        
        response = llm.invoke(prompt)
        return response.content
    
    def _execute_programming(self, description: str, requirements: str, llm) -> str:
        """执行编程任务"""
        prompt = f"""
        请根据以下要求编写代码：
        
        任务描述：{description}
        技术要求：{requirements}
        
        请编写高质量的代码，确保：
        1. 代码功能完整且正确
        2. 代码结构清晰，注释详细
        3. 遵循最佳编程实践
        4. 考虑错误处理和边界情况
        
        请直接输出代码：
        """
        
        response = llm.invoke(prompt)
        return response.content
    
    def _execute_design(self, description: str, requirements: str, llm) -> str:
        """执行设计任务"""
        prompt = f"""
        请根据以下要求进行设计：
        
        任务描述：{description}
        设计要求：{requirements}
        
        请提供详细的设计方案，包括：
        1. 设计理念和思路
        2. 具体的设计元素和布局
        3. 色彩搭配和视觉风格
        4. 用户体验考虑
        5. 技术实现建议
        
        请直接输出设计方案：
        """
        
        response = llm.invoke(prompt)
        return response.content
    
    def _execute_translation(self, description: str, requirements: str, llm) -> str:
        """执行翻译任务"""
        prompt = f"""
        请根据以下要求进行翻译：
        
        任务描述：{description}
        翻译要求：{requirements}
        
        请提供高质量的翻译，确保：
        1. 翻译准确，保持原意
        2. 语言流畅，符合目标语言习惯
        3. 专业术语翻译准确
        4. 文化背景考虑适当
        
        请直接输出翻译结果：
        """
        
        response = llm.invoke(prompt)
        return response.content
    
    def _execute_research(self, description: str, requirements: str, llm) -> str:
        """执行研究任务"""
        prompt = f"""
        请根据以下要求进行研究分析：
        
        任务描述：{description}
        研究要求：{requirements}
        
        请提供详细的研究报告，包括：
        1. 研究背景和目的
        2. 研究方法论
        3. 数据收集和分析
        4. 主要发现和结论
        5. 建议和展望
        
        请直接输出研究报告：
        """
        
        response = llm.invoke(prompt)
        return response.content
    
    def _execute_general_task(self, description: str, requirements: str, llm) -> str:
        """执行通用任务"""
        prompt = f"""
        请根据以下要求完成任务：
        
        任务描述：{description}
        具体要求：{requirements}
        
        请提供高质量的工作成果，确保：
        1. 完全理解任务要求
        2. 提供详细且准确的解决方案
        3. 考虑各种可能的情况
        4. 提供清晰的说明和解释
        
        请直接输出工作成果：
        """
        
        response = llm.invoke(prompt)
        return response.content

class TaskAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="deepseek-v3-250324",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3"
        )
        
        self.blockchain_client = BlockchainClient()
        
        # 初始化工具
        self.tools = [
            TaskAnalysisTool(),
            TaskExecutionTool()
        ]
        
        # 设置Agent提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的AI工作代理，专门负责在区块链上认领和执行任务。

你的主要职责：
1. 分析可用任务，评估是否适合执行
2. 认领合适的任务
3. 高质量地完成任务
4. 提交任务结果并获得报酬

工作流程：
1. 首先分析任务内容和要求
2. 评估任务难度和所需技能
3. 如果任务合适，立即认领
4. 执行任务并生成高质量结果
5. 提交结果到区块链

请始终保持专业和高效的工作态度。"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 创建Agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建Agent执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10
        )
        
        # 初始化记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    async def work_cycle(self) -> Dict[str, Any]:
        """执行一个完整的工作周期"""
        try:
            # 1. 获取可用任务
            available_tasks = self.blockchain_client.get_available_tasks()
            
            if not available_tasks:
                return {
                    "status": "no_tasks",
                    "message": "当前没有可用的任务"
                }
            
            # 2. 分析任务并选择最佳任务
            selected_task = await self._select_best_task(available_tasks)
            
            if not selected_task:
                return {
                    "status": "no_suitable_task",
                    "message": "没有找到合适的任务"
                }
            
            # 3. 认领任务
            claim_success = self.blockchain_client.claim_task(selected_task['id'])
            
            if not claim_success:
                return {
                    "status": "claim_failed",
                    "message": "任务认领失败"
                }
            
            # 4. 执行任务
            task_result = await self._execute_task(selected_task)
            
            # 5. 提交结果
            submit_success = self.blockchain_client.complete_task(
                selected_task['id'], 
                task_result
            )
            
            if submit_success:
                return {
                    "status": "success",
                    "task_id": selected_task['id'],
                    "task_title": selected_task['title'],
                    "reward": selected_task['reward'],
                    "result": task_result
                }
            else:
                return {
                    "status": "submit_failed",
                    "message": "任务提交失败"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"工作周期执行失败: {str(e)}"
            }
    
    async def _select_best_task(self, task_ids: List[int]) -> Optional[Dict]:
        """选择最佳任务"""
        best_task = None
        best_score = 0
        
        for task_id in task_ids:
            task = self.blockchain_client.get_task(task_id)
            if not task:
                continue
            
            # 计算任务评分
            score = self._calculate_task_score(task)
            
            if score > best_score:
                best_score = score
                best_task = task
        
        return best_task
    
    def _calculate_task_score(self, task: Dict) -> float:
        """计算任务评分"""
        score = 0
        
        # 基础分数
        score += 10
        
        # 奖励分数（按比例）
        reward_wei = task['reward']
        reward_eth = reward_wei / 10**18  # 转换为ETH
        score += reward_eth * 100  # 每0.01 ETH加1分
        
        # 时间紧迫性分数
        deadline = task['deadline']
        current_time = int(datetime.now().timestamp())
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
            score += 20  # 内容写作任务
        elif 'programming' in task_type or 'code' in task_type:
            score += 15  # 编程任务
        elif 'research' in task_type:
            score += 10  # 研究任务
        
        return score
    
    async def _execute_task(self, task: Dict) -> str:
        """执行具体任务"""
        # 构建任务信息
        task_info = {
            "task_type": task.get('taskType', 'general'),
            "description": task['description'],
            "requirements": task.get('requirements', ''),
            "title": task['title']
        }
        
        # 使用Agent执行任务
        result = await self.agent_executor.ainvoke({
            "input": f"请执行以下任务：\n任务标题：{task['title']}\n任务描述：{task['description']}\n任务要求：{task.get('requirements', '无特殊要求')}\n\n请分析任务并执行，确保输出高质量的结果。",
            "chat_history": []
        })
        
        return result["output"]
    
    def get_worker_stats(self) -> Dict[str, Any]:
        """获取工人统计信息"""
        worker_address = self.blockchain_client.get_account_address()
        worker_info = self.blockchain_client.get_worker_info(worker_address)
        
        if worker_info:
            return {
                "address": worker_info['addr'],
                "reputation": worker_info['reputation'],
                "completed_tasks": worker_info['completedTasks'],
                "total_earnings": worker_info['totalEarnings'],
                "is_active": worker_info['isActive']
            }
        else:
            return {
                "address": worker_address,
                "reputation": 0,
                "completed_tasks": 0,
                "total_earnings": 0,
                "is_active": False
            }
    
    def get_balance(self) -> int:
        """获取账户余额"""
        return self.blockchain_client.get_balance(
            self.blockchain_client.get_account_address()
        ) 