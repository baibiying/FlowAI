// FlowAI 前端应用
class FlowAIApp {
    constructor() {
        this.apiBase = '/api';
        this.currentTask = null;
        this.autoWorkInterval = null;
        this.claimedTasks = [];
        this.walletConnected = false; // 添加钱包连接状态
        this.walletAddress = null; // 添加钱包地址
        this.currentSortBy = 'default'; // 添加当前排序方式
        this.allTasks = []; // 添加所有任务的缓存
        this.performanceChart = null; // 添加图表实例
        this.currentChartType = 'earnings'; // 当前图表类型
        this.currentTimeRange = 'day'; // 当前时间范围
        
        // 任务标题的多语言映射
        this.taskTitleMap = {
            1: {
                zh: '编写技术博客文章',
                en: 'Write Technical Blog Post'
            },
            2: {
                zh: '开发智能合约',
                en: 'Develop Smart Contract'
            },
            3: {
                zh: '设计UI界面',
                en: 'Design UI Interface'
            },
            4: {
                zh: '翻译技术文档',
                en: 'Translate Technical Documentation'
            },
            5: {
                zh: '市场调研报告',
                en: 'Market Research Report'
            }
        };
        
        this.init();
    }

    init() {
        // 初始化国际化
        if (window.i18n) {
            window.i18n.init();
        }
        
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
        
        // 排序选择器事件
        const sortSelect = document.getElementById('sortBy');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.currentSortBy = e.target.value;
                this.applySorting();
            });
        }
        
        // 图表控件事件
        const chartTypeSelect = document.getElementById('chartType');
        if (chartTypeSelect) {
            chartTypeSelect.addEventListener('change', (e) => {
                this.currentChartType = e.target.value;
                this.updateChart();
            });
        }
        
        const timeRangeSelect = document.getElementById('timeRange');
        if (timeRangeSelect) {
            timeRangeSelect.addEventListener('change', (e) => {
                this.currentTimeRange = e.target.value;
                this.updateChart();
            });
        }

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
        
        // 如果切换到钱包页面，初始化图表
        if (sectionId === 'wallet') {
            setTimeout(() => {
                this.initChart();
            }, 100);
        }
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
            this.addLogEntry('系统', 'log.loadFailed');
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
            
            // 更新图表数据
            if (this.performanceChart) {
                this.updateChart();
            }
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

            // 获取国际化文本
            const connectedText = window.i18n ? window.i18n.t('network.connected') : '已连接';
            const disconnectedText = window.i18n ? window.i18n.t('network.disconnected') : '未连接';
            const connectionFailedText = window.i18n ? window.i18n.t('network.connectionFailed') : '连接失败';
            const gweiText = window.i18n ? window.i18n.t('network.gwei') : 'Gwei';

            document.getElementById('blockchainStatus').textContent = networkInfo.is_connected ? connectedText : disconnectedText;
            document.getElementById('networkId').textContent = networkInfo.chain_id;
            document.getElementById('blockNumber').textContent = networkInfo.block_number;
            document.getElementById('gasPrice').textContent = `${(networkInfo.gas_price / 1e9).toFixed(2)} ${gweiText}`;

            // 更新状态颜色
            const statusElement = document.getElementById('blockchainStatus');
            if (networkInfo.is_connected) {
                statusElement.style.color = '#28a745';
            } else {
                statusElement.style.color = '#dc3545';
            }
        } catch (error) {
            console.error('加载网络信息失败:', error);
            const connectionFailedText = window.i18n ? window.i18n.t('network.connectionFailed') : '连接失败';
            document.getElementById('blockchainStatus').textContent = connectionFailedText;
            document.getElementById('blockchainStatus').style.color = '#dc3545';
        }
    }

    async loadTasks() {
        try {
            // 获取当前语言
            const currentLang = window.i18n ? window.i18n.currentLanguage : 'zh';
            const response = await fetch(`${this.apiBase}/tasks/available?lang=${currentLang}`);
            const tasks = await response.json();

            // 缓存所有任务
            this.allTasks = tasks;

            // 应用排序和过滤
            this.applySorting();
        } catch (error) {
            console.error('加载任务失败:', error);
            this.showNotification('notification.loadFailed', 'error');
        }
    }

    // 应用排序和显示任务
    applySorting() {
            const tasksContainer = document.getElementById('tasksList');
            tasksContainer.innerHTML = '';

        // 过滤掉已经认领的任务
        let availableTasks = this.allTasks.filter(task => 
            !this.claimedTasks.some(claimedTask => claimedTask.id === task.id)
        );

        if (availableTasks.length === 0) {
            const noTasksText = window.i18n ? window.i18n.t('tasks.noTasks') : '当前没有可用的任务';
            tasksContainer.innerHTML = `<p style="text-align: center; color: #666; grid-column: 1 / -1;">${noTasksText}</p>`;
                return;
            }

        // 根据当前排序方式排序任务
        switch (this.currentSortBy) {
            case 'price-high':
                availableTasks.sort((a, b) => b.reward - a.reward);
                break;
            case 'price-low':
                availableTasks.sort((a, b) => a.reward - b.reward);
                break;
            case 'category':
                availableTasks.sort((a, b) => a.task_type.localeCompare(b.task_type));
                break;
            case 'default':
            default:
                // 默认按任务ID排序
                availableTasks.sort((a, b) => a.id - b.id);
                break;
        }

        // 显示排序后的任务
        availableTasks.forEach(task => {
                const taskCard = this.createTaskCard(task);
                tasksContainer.appendChild(taskCard);
            });
    }

    createTaskCard(task) {
        const card = document.createElement('div');
        card.className = 'task-card';
        card.addEventListener('click', () => this.showTaskModal(task));

        const rewardEth = (task.reward / 1e18).toFixed(4);
        const deadline = new Date(task.deadline * 1000).toLocaleString();
        
        // 获取国际化文本
        const deadlineText = window.i18n ? window.i18n.t('tasks.deadline') : '截止时间';
        const publisherText = window.i18n ? window.i18n.t('tasks.publisher') : '发布者';

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
                <span>${deadlineText}: ${deadline}</span>
                <span>${publisherText}: ${task.publisher.substring(0, 8)}...</span>
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
        
        // 获取国际化文本
        const taskDescriptionText = window.i18n ? window.i18n.t('modal.taskDescription') : '任务描述';
        const taskRequirementsText = window.i18n ? window.i18n.t('modal.taskRequirements') : '任务要求';
        const taskTypeText = window.i18n ? window.i18n.t('modal.taskType') : '任务类型';
        const rewardText = window.i18n ? window.i18n.t('modal.reward') : '奖励';
        const deadlineText = window.i18n ? window.i18n.t('modal.deadline') : '截止时间';
        const publisherText = window.i18n ? window.i18n.t('modal.publisher') : '发布者';
        const noRequirementsText = window.i18n ? window.i18n.t('modal.noRequirements') : '无特殊要求';

        modalContent.innerHTML = `
            <div style="margin-bottom: 1rem;">
                <strong>${taskDescriptionText}:</strong>
                <p>${task.description}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>${taskRequirementsText}:</strong>
                <p>${task.requirements || noRequirementsText}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>${taskTypeText}:</strong>
                <p>${task.task_type}</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>${rewardText}:</strong>
                <p>${rewardEth} ETH</p>
            </div>
            <div style="margin-bottom: 1rem;">
                <strong>${deadlineText}:</strong>
                <p>${deadline}</p>
            </div>
            <div>
                <strong>${publisherText}:</strong>
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
                this.showNotification('notification.taskClaimed', 'success');
                
                // 获取任务的原始多语言数据
                try {
                    const rawTaskResponse = await fetch(`${this.apiBase}/tasks/${this.currentTask.id}/raw`);
                    if (rawTaskResponse.ok) {
                        const rawTaskData = await rawTaskResponse.json();
                        // 将原始多语言数据添加到已认领任务数组
                        this.claimedTasks.push(rawTaskData);
                    } else {
                        // 如果获取原始数据失败，使用当前任务数据
                        this.claimedTasks.push(this.currentTask);
                    }
                } catch (error) {
                    console.error('获取任务原始数据失败:', error);
                    this.claimedTasks.push(this.currentTask);
                }
                
                this.updateClaimedTasksDisplay();
                
                this.closeModal();
                this.loadTasks(); // 刷新任务列表
            } else {
                const error = await response.json();
                this.showNotification(`认领失败: ${error.detail}`, 'error');
            }
        } catch (error) {
            console.error('认领任务失败:', error);
            this.showNotification('认领任务失败', 'error');
        }
    }

    updateClaimedTasksDisplay() {
        const claimedTasksList = document.getElementById('claimedTasksList');
        if (!claimedTasksList) return;

        if (this.claimedTasks.length === 0) {
            const noTasksText = window.i18n ? window.i18n.t('agent.noClaimedTasks') : '暂无已认领的任务';
            claimedTasksList.innerHTML = `<p class="no-tasks">${noTasksText}</p>`;
            return;
        }

        // 获取国际化文本
        const rewardText = window.i18n ? window.i18n.t('tasks.reward') : '奖励';
        const taskIdText = window.i18n ? window.i18n.t('tasks.taskId') : '任务ID';

        claimedTasksList.innerHTML = this.claimedTasks.map(task => {
            // 获取当前语言的任务标题
            const currentLang = window.i18n ? window.i18n.currentLanguage : 'zh';
            let taskTitle = task.title || '未知任务';
            
            // 优先使用任务标题映射表
            if (this.taskTitleMap[task.id] && this.taskTitleMap[task.id][currentLang]) {
                taskTitle = this.taskTitleMap[task.id][currentLang];
            } else if (typeof task.title === 'object' && task.title[currentLang]) {
                taskTitle = task.title[currentLang];
            } else if (typeof task.title === 'string') {
                taskTitle = task.title;
            }
            
            return `
                <div class="claimed-task-item">
                    <div class="claimed-task-info">
                        <div class="claimed-task-title">${taskTitle}</div>
                        <div class="claimed-task-reward">${rewardText}: ${(task.reward / 1e18).toFixed(4)} ETH</div>
                        <div class="claimed-task-id">${taskIdText}: ${task.id}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    async startWork() {
        try {
            const response = await fetch(`${this.apiBase}/agent/work`, {
                method: 'POST'
            });

            if (response.ok) {
                this.showNotification('notification.workStarted', 'success');
                this.addLogEntry('系统', 'log.agentStarted');
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
            this.addLogEntry('系统', 'log.startingWork');
            console.log('开始执行工作周期...');
            console.log('当前已认领任务数量:', this.claimedTasks.length);
            console.log('当前已认领任务:', this.claimedTasks);
            
            let response;
            
            // 检查是否有已认领的任务
            if (this.claimedTasks.length > 0) {
                const claimedTaskIds = this.claimedTasks.map(task => task.id);
                this.addLogEntry('AI Agent', 'log.foundClaimedTasks', { 
                    count: this.claimedTasks.length, 
                    ids: claimedTaskIds.join(', ') 
                });
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
                this.addLogEntry('AI Agent', 'log.noClaimedTasks');
                
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
                
                // 获取当前语言的任务标题
                const currentLang = window.i18n ? window.i18n.currentLanguage : 'zh';
                let taskTitle = result.task_title;
                
                // 使用任务标题映射表获取多语言标题
                if (this.taskTitleMap[result.task_id] && this.taskTitleMap[result.task_id][currentLang]) {
                    taskTitle = this.taskTitleMap[result.task_id][currentLang];
                }
                
                // 记录任务认领
                this.addLogEntry('AI Agent', 'log.taskClaimed', { 
                    title: taskTitle, 
                    id: result.task_id 
                });
                
                // 记录任务执行
                this.addLogEntry('AI Agent', 'log.taskExecuting', { title: taskTitle });
                
                // 记录任务完成
                this.addLogEntry('AI Agent', 'log.taskCompleted', { title: taskTitle });
                this.addLogEntry('AI Agent', 'log.taskReward', { reward: rewardEth });
                
                // 从已认领任务列表中移除已完成的任务
                this.claimedTasks = this.claimedTasks.filter(task => task.id !== result.task_id);
                this.updateClaimedTasksDisplay();
                
                this.showNotification(`notification.taskCompleted`, 'success', { reward: rewardEth });
                console.log('任务完成，刷新统计数据...');
                await this.loadStats(); // 等待统计数据刷新完成
                await this.loadBalance(); // 同时刷新余额
                
                // 强制更新图表
                if (this.performanceChart) {
                    setTimeout(() => {
                        this.updateChart();
                    }, 100);
                }
                
                console.log('统计数据刷新完成');
            } else if (result.status === 'no_tasks') {
                this.addLogEntry('AI Agent', 'log.noAvailableTasks');
                this.showNotification('notification.noTasks', 'info');
            } else if (result.status === 'no_suitable_task') {
                this.addLogEntry('AI Agent', 'log.noSuitableTasks');
                this.showNotification('notification.noSuitableTask', 'info');
            } else {
                this.showNotification(result.message, 'info');
                this.addLogEntry('AI Agent', result.message);
            }
        } catch (error) {
            console.error('执行工作周期失败:', error);
            this.showNotification('执行工作周期失败', 'error');
            this.addLogEntry('系统', 'log.workFailed');
        }
    }

    startAutoWork() {
        if (this.autoWorkInterval) return;

        this.autoWorkInterval = setInterval(() => {
            this.executeWorkCycle();
        }, 30000); // 每30秒执行一次

        document.getElementById('startAutoWork').disabled = true;
        document.getElementById('stopAutoWork').disabled = false;
        
        this.showNotification('notification.autoWorkStarted', 'success');
        this.addLogEntry('系统', 'log.autoWorkStarted');
    }

    stopAutoWork() {
        if (this.autoWorkInterval) {
            clearInterval(this.autoWorkInterval);
            this.autoWorkInterval = null;
        }

        document.getElementById('startAutoWork').disabled = false;
        document.getElementById('stopAutoWork').disabled = true;
        
        this.showNotification('notification.autoWorkStopped', 'info');
        this.addLogEntry('系统', 'log.autoWorkStopped');
    }

    async refreshStats() {
        await Promise.all([
            this.loadStats(),
            this.loadBalance(),
            this.loadNetworkInfo()
        ]);
        this.showNotification('notification.statsRefreshed', 'success');
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
        try {
            // 检查是否支持MetaMask
            if (typeof window.ethereum !== 'undefined') {
                // 请求连接钱包
                const accounts = await window.ethereum.request({ 
                    method: 'eth_requestAccounts' 
                });
                
                if (accounts.length > 0) {
                    const address = accounts[0];
                    
                    // 更新应用状态
                    this.walletConnected = true;
                    this.walletAddress = address;
                    
                    // 更新UI显示
                    const accountAddressElement = document.getElementById('accountAddress');
                    const connectWalletElement = document.getElementById('connectWallet');
                    
                    if (accountAddressElement) {
                        accountAddressElement.textContent = address;
                    }
                    if (connectWalletElement) {
                        const connectedText = window.i18n ? window.i18n.t('wallet.connected') : '已连接';
                        connectWalletElement.textContent = connectedText;
                        connectWalletElement.disabled = true;
                    }
                    
                    this.showNotification('notification.walletConnected', 'success');
                    this.addLogEntry('系统', 'log.walletConnected', { 
                        address: `${address.substring(0, 6)}...${address.substring(38)}` 
                    });
                    
                    // 刷新余额和网络信息
                    await this.loadBalance();
                    await this.loadNetworkInfo();
                }
            } else {
                // 如果没有MetaMask，显示模拟连接
                const mockAddress = '0x' + Math.random().toString(16).substr(2, 40);
                
                // 更新应用状态
                this.walletConnected = true;
                this.walletAddress = mockAddress;
                
                const accountAddressElement = document.getElementById('accountAddress');
                const connectWalletElement = document.getElementById('connectWallet');
                
                if (accountAddressElement) {
                    accountAddressElement.textContent = mockAddress;
                }
                if (connectWalletElement) {
                    const connectedText = window.i18n ? window.i18n.t('wallet.connected') : '已连接';
                    connectWalletElement.textContent = connectedText;
                    connectWalletElement.disabled = true;
                }
                
                this.showNotification('notification.mockWalletConnected', 'success');
                this.addLogEntry('系统', 'log.walletConnected', { 
                    address: `${mockAddress.substring(0, 6)}...${mockAddress.substring(38)}` 
                });
                
                // 刷新余额和网络信息
                await this.loadBalance();
                await this.loadNetworkInfo();
            }
        } catch (error) {
            console.error('钱包连接失败:', error);
            this.showNotification('钱包连接失败，请重试', 'error');
        }
    }

    copyAddress() {
        const address = document.getElementById('accountAddress').textContent;
        if (address && address !== '未连接') {
            navigator.clipboard.writeText(address).then(() => {
                this.showNotification('notification.addressCopied', 'success');
                this.addLogEntry('系统', 'log.addressCopied');
            });
        }
    }

    // 更新钱包显示状态
    updateWalletDisplay() {
        if (this.walletConnected && this.walletAddress) {
            // 更新地址显示
            const accountAddressElement = document.getElementById('accountAddress');
            if (accountAddressElement) {
                accountAddressElement.textContent = this.walletAddress;
            }
            
            // 更新连接按钮状态
            const connectWalletElement = document.getElementById('connectWallet');
            if (connectWalletElement) {
                const connectedText = window.i18n ? window.i18n.t('wallet.connected') : '已连接';
                connectWalletElement.textContent = connectedText;
                connectWalletElement.disabled = true;
            }
        }
    }

    // 初始化图表
    initChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        this.performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });
        
        this.updateChart();
    }

    // 更新图表数据
    updateChart() {
        if (!this.performanceChart) return;

        const data = this.generateChartData();
        
        this.performanceChart.data.labels = data.labels;
        this.performanceChart.data.datasets[0].data = data.values;
        this.performanceChart.data.datasets[0].label = data.label;
        
        this.performanceChart.update();
    }

    // 生成图表数据
    generateChartData() {
        const currentLang = window.i18n ? window.i18n.currentLanguage : 'zh';
        
        let labels = [];
        let values = [];
        let label = '';

        if (this.currentChartType === 'earnings') {
            label = currentLang === 'zh' ? '收入 (ETH)' : 'Earnings (ETH)';
        } else {
            label = currentLang === 'zh' ? '完成任务数' : 'Tasks Completed';
        }

        // 获取当前完成的任务数量和收入
        const completedTasksElement = document.getElementById('completedTasks');
        const totalEarningsElement = document.getElementById('totalEarnings');
        
        let completedTasks = 0;
        let totalEarnings = 0;
        
        if (completedTasksElement) {
            completedTasks = parseInt(completedTasksElement.textContent) || 0;
        }
        
        if (totalEarningsElement) {
            const earningsText = totalEarningsElement.textContent;
            totalEarnings = parseFloat(earningsText.replace(' ETH', '')) || 0;
        }

        console.log('图表数据 - 完成任务数:', completedTasks, '总收入:', totalEarnings);

        // 获取当前日期
        const now = new Date();
        
        // 根据实际完成情况生成数据
        switch (this.currentTimeRange) {
            case 'day':
                // 生成最近7天的日期，格式：2025/08/12
                labels = [];
                for (let i = 6; i >= 0; i--) {
                    const date = new Date(now);
                    date.setDate(date.getDate() - i);
                    const year = date.getFullYear();
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const day = String(date.getDate()).padStart(2, '0');
                    labels.push(`${year}/${month}/${day}`);
                }
                
                // 所有数据都放在今天（最后一个时间点）
                if (this.currentChartType === 'earnings') {
                    values = [0, 0, 0, 0, 0, 0, totalEarnings];
                } else {
                    values = [0, 0, 0, 0, 0, 0, completedTasks];
                }
                break;
                
            case 'month':
                // 生成最近12个月的日期，格式：2025/08
                labels = [];
                for (let i = 11; i >= 0; i--) {
                    const date = new Date(now);
                    date.setMonth(date.getMonth() - i);
                    const year = date.getFullYear();
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    labels.push(`${year}/${month}`);
                }
                
                // 所有数据都放在当前月（最后一个时间点）
                if (this.currentChartType === 'earnings') {
                    values = new Array(11).fill(0).concat([totalEarnings]);
                } else {
                    values = new Array(11).fill(0).concat([completedTasks]);
                }
                break;
                
            case 'quarter':
                // 生成最近4个季度的日期，格式：2025/Q1
                labels = [];
                for (let i = 3; i >= 0; i--) {
                    const date = new Date(now);
                    date.setMonth(date.getMonth() - (i * 3));
                    const year = date.getFullYear();
                    const quarter = Math.floor(date.getMonth() / 3) + 1;
                    labels.push(`${year}/Q${quarter}`);
                }
                
                // 所有数据都放在当前季度（最后一个时间点）
                if (this.currentChartType === 'earnings') {
                    values = [0, 0, 0, totalEarnings];
                } else {
                    values = [0, 0, 0, completedTasks];
                }
                break;
                
            case 'year':
                // 生成最近5年的日期，格式：2025
                labels = [];
                for (let i = 4; i >= 0; i--) {
                    const date = new Date(now);
                    date.setFullYear(date.getFullYear() - i);
                    const year = date.getFullYear();
                    labels.push(`${year}`);
                }
                
                // 所有数据都放在当前年（最后一个时间点）
                if (this.currentChartType === 'earnings') {
                    values = new Array(4).fill(0).concat([totalEarnings]);
                } else {
                    values = new Array(4).fill(0).concat([completedTasks]);
                }
                break;
        }

        console.log('生成的图表数据:', { labels, values, label });
        return { labels, values, label };
    }

    addLogEntry(time, message, params = {}) {
        const logContainer = document.getElementById('agentLog');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        const now = new Date().toLocaleTimeString();
        
        // 如果message是国际化key，则翻译
        if (window.i18n && message.startsWith('log.')) {
            message = window.i18n.t(message, params);
        }
        
        logEntry.innerHTML = `
            <span class="log-time">${now}</span>
            <span class="log-message">${message}</span>
        `;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    showNotification(message, type = 'info', params = {}) {
        const notification = document.getElementById('notification');
        const messageElement = document.getElementById('notificationMessage');
        
        // 如果message是国际化key，则翻译
        if (window.i18n && message.startsWith('notification.')) {
            message = window.i18n.t(message, params);
        }
        
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
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.flowAIApp = new FlowAIApp();
});

// 全局函数
function closeModal() {
    window.flowAIApp.closeModal();
} 