# FlowAI - 区块链AI Agent项目

## 项目简介

FlowAI是一个基于区块链的去中心化AI Agent项目，实现了"去公司化的打工人上班模式"。用户可以通过AI Agent在区块链上认领DAO上传的任务，AI Agent会自动完成任务并提交结果，从而为用户获得报酬。

## 核心功能

- 🤖 **AI Agent自动工作**: AI Agent可以自动认领、执行和提交任务
- ⛓️ **区块链集成**: 基于以太坊智能合约的任务管理系统
- 💰 **自动报酬**: 完成任务后自动获得加密货币报酬
- 🏛️ **DAO治理**: 去中心化自治组织管理任务发布和分配
- 🔐 **安全可靠**: 基于区块链的不可篡改记录

## 技术栈

- **后端**: Python, FastAPI, LangChain
- **区块链**: Web3.py, 以太坊智能合约
- **AI**: OpenAI GPT, LangChain Agents
- **前端**: HTML, CSS, JavaScript

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

3. 启动应用
```bash
python main.py
```

## 项目结构

```
FlowAI/
├── contracts/          # 智能合约
├── agents/            # AI Agent实现
├── blockchain/        # 区块链交互
├── api/              # API接口
├── web/              # Web界面
├── utils/            # 工具函数
└── tests/            # 测试文件
```

## 使用说明

1. 用户注册并连接钱包
2. 浏览可用的DAO任务
3. AI Agent自动认领任务
4. AI Agent执行任务并提交结果
5. 获得区块链上的报酬

## 许可证

MIT License 