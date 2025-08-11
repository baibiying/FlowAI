// FlowAI 前端应用
class FlowAIApp {
    constructor() {
        this.apiBase = '/api';
        this.currentTask = null;
        this.autoWorkInterval = null;
        this.claimedTasks = []; // 存储已认领的任务
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupNavigation();
    }

    setupEventListeners() {
        // 导航事件
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateToSection(e.target.getAttribute('href').substring(1));
            });
        });

        // 按钮事件
        document.getElementById('connectWallet').addEventListener('click', () => this.connectWallet());
        document.getElementById('startWork').addEventListener('click', () => this.startWork());
        document.getElementById('refreshStats').addEventListener('click', () => this.refreshStats());
        document.getElementById('refreshTasks').addEventListener('click', () => this.loadTasks());
        document.getElementById('startAutoWork').addEventListener('click', () => this.startAutoWork());
        document.getElementById('stopAutoWork').addEventListener('click', () => this.stopAutoWork());
        document.getElementById('executeWorkCycle').addEventListener('click', () => this.executeWorkCycle());
        document.getElementById('copyAddress').addEventListener('click', () => this.copyAddress());

        // 模态框事件
        const closeBtn = document.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal());
        }
        
        const claimTaskBtn = document.getElementById('claimTask');
        if (claimTaskBtn) {
            claimTaskBtn.addEventListener('click', () => this.claimCurrentTask());
        }
        
        const notificationCloseBtn = document.querySelector('.notification-close');
        if (notificationCloseBtn) {
            notificationCloseBtn.addEventListener('click', () => this.hideNotification());
        }

        // 点击模态框外部关闭
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal();
            }
        });
    }

    setupNavigation() {
        // 默认显示仪表板
        this.navigateToSection('dashboard');
    }

    navigateToSection(sectionId) {
        // 隐藏所有section
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // 显示目标section
        document.getElementById(sectionId).classList.add('active');

        // 更新导航链接状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadStats(),
                this.loadBalance(),
                this.loadNetworkInfo(),
                this.loadTasks(),
                this.loadAccountInfo()
            ]);
        } catch (error) {
            console.error('加载初始数据失败:', error);
            this.showNotification('加载数据失败，请检查网络连接', 'error');
        }
    }

    async loadStats() {
        try {
            const response = await fetch(`${this.apiBase}/worker/stats`);
            const stats = await response.json();

            document.getElementById('reputation').textContent = stats.reputation;
            document.getElementById('completedTasks').textContent = stats.completed_tasks;
            document.getElementById('totalEarnings').textContent = `${(stats.total_earnings / 1e18).toFixed(4)} ETH`;

            // 更新钱包页面
            document.getElementById('walletReputation').textContent = stats.reputation;
            document.getElementById('walletCompletedTasks').textContent = stats.completed_tasks;
            document.getElementById('walletTotalEarnings').textContent = `${(stats.total_earnings / 1e18).toFixed(4)} ETH`;
        } catch (error) {
            console.error('加载统计信息失败:', error);
        }
    }

    async loadBalance() {
        try {
            console.log('正在加载余额...');
            const response = await fetch(`${this.apiBase}/worker/balance`);
            const balance = await response.json();
            console.log('余额数据:', balance);

            document.getElementById('balance').textContent = `${balance.balance_eth.toFixed(4)} ETH`;
            document.getElementById('ethBalance').textContent = balance.balance_eth.toFixed(4);
            document.getElementById('weiBalance').textContent = balance.balance_wei;
            
            console.log('余额加载完成');
        } catch (error) {
            console.error('加载余额失败:', error);
        }
    }

    async loadNetworkInfo() {
        try {
            const response = await fetch(`${this.apiBase}/network/info`);
            const networkInfo = await response.json();

            document.getElementById('blockchainStatus').textContent = networkInfo.is_connected ? '已连接' : '未连接';
            document.getElementById('networkId').textContent = networkInfo.chain_id;
            document.getElementById('blockNumber').textContent = networkInfo.block_number;
            document.getElementById('gasPrice').textContent = `${(networkInfo.gas_price / 1e9).toFixed(2)} Gwei`;

            // 更新状态颜色
            const statusElement = document.getElementById('blockchainStatus');
            if (networkInfo.is_connected) {
                statusElement.style.color = '#28a745';
            } else {
                statusElement.style.color = '#dc3545';
            }
        } catch (error) {
            console.error('加载网络信息失败:', error);
            document.getElementById('blockchainStatus').textContent = '连接失败';
            document.getElementById('blockchainStatus').style.color = '#dc3545';
        }
    }

    async loadTasks() {
        try {
            const response = await fetch(`${this.apiBase}/tasks/available`);
            const tasks = await response.json();

            const tasksContainer = document.getElementById('tasksList');
            tasksContainer.innerHTML = '';

            // 过滤掉已认领的任务
            const claimedTaskIds = this.claimedTasks.map(task => task.id);
            const availableTasks = tasks.filter(task => !claimedTaskIds.includes(task.id));

            if (availableTasks.length === 0) {
                tasksContainer.innerHTML = '<p style="text-align: center; color: #666; grid-column: 1 / -1;">当前没有可用的任务</p>';
                return;
            }

            availableTasks.forEach(task => {
                const taskCard = this.createTaskCard(task);
                tasksContainer.appendChild(taskCard);
            });
        } catch (error) {
            console.error('加载任务失败:', error);
            this.showNotification('加载任务失败', 'error');
        }
    }

    createTaskCard(task) {
        const card = document.createElement('div');
        card.className = 'task-card';
        card.addEventListener('click', () => this.showTaskModal(task));

        const rewardEth = (task.reward / 1e18).toFixed(4);
        const deadline = new Date(task.deadline * 1000).toLocaleString();

        card.innerHTML = `
            <div class="task-header">
                <div>
                    <div class="task-title">${task.title}</div>
                    <div class="task-type">${task.task_type}</div>
                </div>
                <div class="task-reward">${rewardEth} ETH</div>
            </div>
            <div class="task-description">${task.description.substring(0, 150)}${task.description.length > 150 ? '...' : ''}</div>
            <div class="task-meta">
                <span>截止时间: ${deadline}</span>
                <span>发布者: ${task.publisher.substring(0, 8)}...</span>
            </div>
        `;

        return card;
    }

    showTaskModal(task) {
        this.currentTask = task;
        const modal = document.getElementById('taskModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalContent = document.getElementById('modalContent');

        modalTitle.textContent = task.title;

        const rewardEth = (task.reward / 1e18).toFixed(4);
        const deadline = new Date(task.deadline * 1000).toLocaleString();

        modalContent.innerHTML = `
            <div style="margin-bottom: 1rem;">
                <strong>任务描述:</strong>
                <p>${task.description}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>任务要求:</strong>
                <p>${task.requirements || '无特殊要求'}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>任务类型:</strong>
                <p>${task.task_type}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>奖励:</strong>
                <p>${rewardEth} ETH</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>截止时间:</strong>
                <p>${deadline}</p>
            </div>
            <div>
                <strong>发布者:</strong>
                <p>${task.publisher}</p>
            </div>
        `;

        modal.style.display = 'block';
    }

    closeModal() {
        document.getElementById('taskModal').style.display = 'none';
        this.currentTask = null;
    }

    async claimCurrentTask() {
        if (!this.currentTask) return;

        try {
            const response = await fetch(`${this.apiBase}/tasks/${this.currentTask.id}/claim`, {
                method: 'POST'
            });

            if (response.ok) {
                // 将认领的任务添加到已认领任务数组
                this.claimedTasks.push(this.currentTask);
                this.showNotification('任务认领成功！已添加到待执行队列', 'success');
                this.closeModal();
                this.loadTasks(); // 刷新任务列表
                this.updateClaimedTasksDisplay(); // 更新已认领任务显示
            } else {
                const error = await response.json();
                this.showNotification(`认领失败: ${error.detail}`, 'error');
            }
        } catch (error) {
            console.error('认领任务失败:', error);
            this.showNotification('认领任务失败', 'error');
        }
    }

    async startWork() {
        try {
            const response = await fetch(`${this.apiBase}/agent/work`, {
                method: 'POST'
            });

            if (response.ok) {
                this.showNotification('AI Agent已开始工作', 'success');
                this.addLogEntry('系统', 'AI Agent开始工作');
            } else {
                const error = await response.json();
                this.showNotification(`启动失败: ${error.detail}`, 'error');
            }
        } catch (error) {
            console.error('启动工作失败:', error);
            this.showNotification('启动工作失败', 'error');
        }
    }

    async executeWorkCycle() {
        try {
            this.addLogEntry('系统', '开始执行工作周期...');
            console.log('开始执行工作周期...');
            console.log('当前已认领任务数量:', this.claimedTasks.length);
            console.log('当前已认领任务:', this.claimedTasks);
            
            let response;
            
            // 检查是否有已认领的任务
            if (this.claimedTasks.length > 0) {
                const claimedTaskIds = this.claimedTasks.map(task => task.id);
                this.addLogEntry('AI Agent', `📋 发现 ${this.claimedTasks.length} 个已认领的任务，优先执行: ${claimedTaskIds.join(', ')}`);
                console.log('发送已认领任务ID:', claimedTaskIds);
                
                // 发送已认领任务信息到后端
                response = await fetch(`${this.apiBase}/agent/work/sync`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        claimed_tasks: claimedTaskIds
                    })
                });
            } else {
                this.addLogEntry('AI Agent', '📭 没有已认领的任务，正在获取可用任务列表...');
                
                response = await fetch(`${this.apiBase}/agent/work/sync`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        claimed_tasks: []
                    })
                });
            }

            const result = await response.json();
            console.log('API返回结果:', result);

            if (result.status === 'success') {
                const rewardEth = (result.reward / 1e18).toFixed(4);
                
                // 从已认领任务数组中移除已完成的任务
                this.claimedTasks = this.claimedTasks.filter(task => task.id !== result.task_id);
                this.updateClaimedTasksDisplay();
                
                // 记录任务认领
                this.addLogEntry('AI Agent', `✅ 认领任务: ${result.task_title} (任务ID: ${result.task_id})`);
                
                // 记录任务执行
                this.addLogEntry('AI Agent', `🔄 开始执行任务: ${result.task_title}`);
                
                // 记录任务完成
                this.addLogEntry('AI Agent', `🎉 完成任务: ${result.task_title}`);
                this.addLogEntry('AI Agent', `💰 获得奖励: ${rewardEth} ETH`);
                
                this.showNotification(`任务完成！获得 ${rewardEth} ETH`, 'success');
                console.log('任务完成，刷新统计数据...');
                await this.loadStats(); // 等待统计数据刷新完成
                await this.loadBalance(); // 同时刷新余额
                console.log('统计数据刷新完成');
            } else if (result.status === 'no_tasks') {
                this.addLogEntry('AI Agent', '📭 当前没有可用的任务');
                this.showNotification('当前没有可用的任务', 'info');
            } else if (result.status === 'no_suitable_task') {
                this.addLogEntry('AI Agent', '🔍 没有找到合适的任务');
                this.showNotification('没有找到合适的任务', 'info');
            } else {
                this.showNotification(result.message, 'info');
                this.addLogEntry('AI Agent', result.message);
            }
        } catch (error) {
            console.error('执行工作周期失败:', error);
            this.showNotification('执行工作周期失败', 'error');
            this.addLogEntry('系统', '❌ 工作周期执行失败');
        }
    }

    startAutoWork() {
        if (this.autoWorkInterval) return;

        this.autoWorkInterval = setInterval(() => {
            this.executeWorkCycle();
        }, 30000); // 每30秒执行一次

        document.getElementById('startAutoWork').disabled = true;
        document.getElementById('stopAutoWork').disabled = false;
        
        this.showNotification('自动工作模式已启动', 'success');
        this.addLogEntry('系统', '启动自动工作模式');
    }

    stopAutoWork() {
        if (this.autoWorkInterval) {
            clearInterval(this.autoWorkInterval);
            this.autoWorkInterval = null;
        }

        document.getElementById('startAutoWork').disabled = false;
        document.getElementById('stopAutoWork').disabled = true;
        
        this.showNotification('自动工作模式已停止', 'info');
        this.addLogEntry('系统', '停止自动工作模式');
        
        // 确保已认领任务和仪表盘数据保持不变
        console.log('停止自动工作模式，已认领任务数量:', this.claimedTasks.length);
        console.log('已认领任务:', this.claimedTasks);
    }

    async refreshStats() {
        await Promise.all([
            this.loadStats(),
            this.loadBalance(),
            this.loadNetworkInfo()
        ]);
        this.showNotification('统计信息已刷新', 'success');
    }

    async loadAccountInfo() {
        try {
            const response = await fetch(`${this.apiBase}/account/address`);
            const account = await response.json();
            
            document.getElementById('accountAddress').textContent = account.address;
        } catch (error) {
            console.error('加载账户信息失败:', error);
        }
    }

    async connectWallet() {
        // 这里可以集成MetaMask或其他钱包
        this.showNotification('钱包连接功能开发中...', 'info');
    }

    copyAddress() {
        const address = document.getElementById('accountAddress').textContent;
        if (address && address !== '未连接') {
            navigator.clipboard.writeText(address).then(() => {
                this.showNotification('地址已复制到剪贴板', 'success');
            });
        }
    }

    addLogEntry(time, message) {
        const logContainer = document.getElementById('agentLog');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        const now = new Date().toLocaleTimeString();
        logEntry.innerHTML = `
            <span class="log-time">${now}</span>
            <span class="log-message">${message}</span>
        `;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        const messageElement = document.getElementById('notificationMessage');
        
        messageElement.textContent = message;
        
        // 设置通知类型样式
        notification.className = `notification notification-${type}`;
        
        notification.style.display = 'block';
        
        // 3秒后自动隐藏
        setTimeout(() => {
            this.hideNotification();
        }, 3000);
    }

    hideNotification() {
        document.getElementById('notification').style.display = 'none';
    }

    updateClaimedTasksDisplay() {
        // 更新已认领任务计数
        const claimedTasksCount = document.getElementById('claimedTasksCount');
        if (claimedTasksCount) {
            claimedTasksCount.textContent = `(${this.claimedTasks.length})`;
        }

        // 更新已认领任务显示
        const claimedTasksContainer = document.getElementById('claimedTasksList');
        if (claimedTasksContainer) {
            if (this.claimedTasks.length === 0) {
                claimedTasksContainer.innerHTML = '<p style="text-align: center; color: #666;">暂无已认领的任务</p>';
            } else {
                claimedTasksContainer.innerHTML = '';
                this.claimedTasks.forEach(task => {
                    const taskItem = document.createElement('div');
                    taskItem.className = 'claimed-task-item';
                    const rewardEth = (task.reward / 1e18).toFixed(4);
                    taskItem.innerHTML = `
                        <div class="task-info">
                            <div class="task-title">${task.title}</div>
                            <div class="task-reward">${rewardEth} ETH</div>
                        </div>
                        <div class="task-description">${task.description.substring(0, 100)}...</div>
                    `;
                    claimedTasksContainer.appendChild(taskItem);
                });
            }
        }
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.flowAIApp = new FlowAIApp();
});

// 全局函数
function closeModal() {
    window.flowAIApp.closeModal();
} 