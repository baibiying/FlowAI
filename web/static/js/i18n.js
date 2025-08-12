// 国际化支持
const i18n = {
    currentLanguage: 'zh', // 默认中文
    
    // 中文翻译
    zh: {
        // 导航
        'nav.dashboard': '仪表板',
        'nav.tasks': '任务市场',
        'nav.agent': 'AI Agent',
        'nav.wallet': '钱包',
        
        // 语言切换
        'lang.en': 'EN',
        'lang.zh': '中文',
        
        // 钱包
        'wallet.connect': '连接钱包',
        'wallet.connected': '已连接',
        'wallet.title': '钱包信息',
        'wallet.accountAddress': '账户地址',
        'wallet.notConnected': '未连接',
        'wallet.copyAddress': '复制地址',
        'wallet.accountBalance': '账户余额',
        'wallet.workStats': '工作统计',
        'wallet.reputation': '声誉值',
        'wallet.completedTasks': '完成任务',
        'wallet.totalEarnings': '总收入',
        
        // 仪表板
        'dashboard.title': '仪表板',
        'dashboard.welcome': '欢迎使用FlowAI - 去中心化的AI工作代理平台',
        'dashboard.balance': '账户余额',
        'dashboard.reputation': '声誉值',
        'dashboard.completedTasks': '完成任务',
        'dashboard.totalEarnings': '总收入',
        'dashboard.startWork': '启动AI Agent工作',
        'dashboard.refreshStats': '刷新统计',
        'dashboard.networkStatus': '网络状态',
        'dashboard.blockchainConnection': '区块链连接',
        'dashboard.checking': '检查中...',
        'dashboard.networkId': '网络ID',
        'dashboard.blockNumber': '区块高度',
        'dashboard.gasPrice': 'Gas价格',
        
        // 任务市场
        'tasks.title': '任务市场',
        'tasks.refresh': '刷新任务',
        'tasks.noTasks': '当前没有可用的任务',
        'tasks.deadline': '截止时间',
        'tasks.publisher': '发布者',
        'tasks.reward': '奖励',
        'tasks.taskId': '任务ID',
        
        // AI Agent
        'agent.title': 'AI Agent控制台',
        'agent.workMode': '工作模式',
        'agent.startAutoWork': '启动自动工作',
        'agent.stopAutoWork': '停止自动工作',
        'agent.manualExecution': '手动执行',
        'agent.executeWorkCycle': '执行工作周期',
        'agent.claimedTasks': '已认领任务',
        'agent.noClaimedTasks': '暂无已认领的任务',
        'agent.workLog': '工作日志',
        'agent.systemStart': '系统启动',
        'agent.agentReady': 'AI Agent已准备就绪',
        
        // 模态框
        'modal.claimTask': '认领任务',
        'modal.close': '关闭',
        'modal.taskDescription': '任务描述',
        'modal.taskRequirements': '任务要求',
        'modal.taskType': '任务类型',
        'modal.reward': '奖励',
        'modal.deadline': '截止时间',
        'modal.publisher': '发布者',
        'modal.noRequirements': '无特殊要求',
        
        // 通知
        'notification.taskClaimed': '任务认领成功！',
        'notification.taskCompleted': '任务完成！获得 {reward} ETH',
        'notification.noTasks': '当前没有可用的任务',
        'notification.noSuitableTask': '没有找到合适的任务',
        'notification.workStarted': 'AI Agent已开始工作',
        'notification.autoWorkStarted': '自动工作模式已启动',
        'notification.autoWorkStopped': '自动工作模式已停止',
        'notification.walletConnected': '钱包连接成功',
        'notification.mockWalletConnected': '模拟钱包连接成功！',
        'notification.addressCopied': '地址已复制到剪贴板',
        'notification.statsRefreshed': '统计信息已刷新',
        'notification.loadFailed': '加载失败',
        'notification.networkError': '网络错误',
        
        // 网络状态
        'network.connected': '已连接',
        'network.disconnected': '未连接',
        'network.connectionFailed': '连接失败',
        'network.gwei': 'Gwei',
        
        // 工作日志
        'log.startingWork': '开始执行工作周期...',
        'log.foundClaimedTasks': '发现 {count} 个已认领的任务，优先执行: {ids}',
        'log.noClaimedTasks': '没有已认领的任务，正在获取可用任务列表...',
        'log.taskClaimed': '✅ 认领任务: {title} (任务ID: {id})',
        'log.taskExecuting': '🔄 开始执行任务: {title}',
        'log.taskCompleted': '🎉 完成任务: {title}',
        'log.taskReward': '💰 获得奖励: {reward} ETH',
        'log.noAvailableTasks': '📭 当前没有可用的任务',
        'log.noSuitableTasks': '🔍 没有找到合适的任务',
        'log.workFailed': '❌ 工作周期执行失败',
        'log.agentStarted': 'AI Agent开始工作',
        'log.autoWorkStarted': '启动自动工作模式',
        'log.autoWorkStopped': '停止自动工作模式',
        'log.walletConnected': '钱包连接成功: {address}',
        'log.addressCopied': '地址已复制到剪贴板',
        'log.loadFailed': '加载数据失败，请检查网络连接'
    },
    
    // 英文翻译
    en: {
        // 导航
        'nav.dashboard': 'Dashboard',
        'nav.tasks': 'Task Market',
        'nav.agent': 'AI Agent',
        'nav.wallet': 'Wallet',
        
        // 语言切换
        'lang.en': 'EN',
        'lang.zh': '中文',
        
        // 钱包
        'wallet.connect': 'Connect Wallet',
        'wallet.connected': 'Connected',
        'wallet.title': 'Wallet Information',
        'wallet.accountAddress': 'Account Address',
        'wallet.notConnected': 'Not Connected',
        'wallet.copyAddress': 'Copy Address',
        'wallet.accountBalance': 'Account Balance',
        'wallet.workStats': 'Work Statistics',
        'wallet.reputation': 'Reputation',
        'wallet.completedTasks': 'Completed Tasks',
        'wallet.totalEarnings': 'Total Earnings',
        
        // 仪表板
        'dashboard.title': 'Dashboard',
        'dashboard.welcome': 'Welcome to FlowAI - Decentralized AI Work Agent Platform',
        'dashboard.balance': 'Account Balance',
        'dashboard.reputation': 'Reputation',
        'dashboard.completedTasks': 'Completed Tasks',
        'dashboard.totalEarnings': 'Total Earnings',
        'dashboard.startWork': 'Start AI Agent Work',
        'dashboard.refreshStats': 'Refresh Stats',
        'dashboard.networkStatus': 'Network Status',
        'dashboard.blockchainConnection': 'Blockchain Connection',
        'dashboard.checking': 'Checking...',
        'dashboard.networkId': 'Network ID',
        'dashboard.blockNumber': 'Block Number',
        'dashboard.gasPrice': 'Gas Price',
        
        // 任务市场
        'tasks.title': 'Task Market',
        'tasks.refresh': 'Refresh Tasks',
        'tasks.noTasks': 'No available tasks',
        'tasks.deadline': 'Deadline',
        'tasks.publisher': 'Publisher',
        'tasks.reward': 'Reward',
        'tasks.taskId': 'Task ID',
        
        // AI Agent
        'agent.title': 'AI Agent Console',
        'agent.workMode': 'Work Mode',
        'agent.startAutoWork': 'Start Auto Work',
        'agent.stopAutoWork': 'Stop Auto Work',
        'agent.manualExecution': 'Manual Execution',
        'agent.executeWorkCycle': 'Execute Work Cycle',
        'agent.claimedTasks': 'Claimed Tasks',
        'agent.noClaimedTasks': 'No claimed tasks',
        'agent.workLog': 'Work Log',
        'agent.systemStart': 'System Start',
        'agent.agentReady': 'AI Agent Ready',
        
        // 模态框
        'modal.claimTask': 'Claim Task',
        'modal.close': 'Close',
        'modal.taskDescription': 'Task Description',
        'modal.taskRequirements': 'Task Requirements',
        'modal.taskType': 'Task Type',
        'modal.reward': 'Reward',
        'modal.deadline': 'Deadline',
        'modal.publisher': 'Publisher',
        'modal.noRequirements': 'No special requirements',
        
        // 通知
        'notification.taskClaimed': 'Task claimed successfully!',
        'notification.taskCompleted': 'Task completed! Earned {reward} ETH',
        'notification.noTasks': 'No available tasks',
        'notification.noSuitableTask': 'No suitable task found',
        'notification.workStarted': 'AI Agent started working',
        'notification.autoWorkStarted': 'Auto work mode started',
        'notification.autoWorkStopped': 'Auto work mode stopped',
        'notification.walletConnected': 'Wallet connected successfully',
        'notification.mockWalletConnected': 'Mock wallet connected successfully!',
        'notification.addressCopied': 'Address copied to clipboard',
        'notification.statsRefreshed': 'Statistics refreshed',
        'notification.loadFailed': 'Load failed',
        'notification.networkError': 'Network error',
        
        // 网络状态
        'network.connected': 'Connected',
        'network.disconnected': 'Disconnected',
        'network.connectionFailed': 'Connection Failed',
        'network.gwei': 'Gwei',
        
        // 工作日志
        'log.startingWork': 'Starting work cycle...',
        'log.foundClaimedTasks': 'Found {count} claimed tasks, prioritizing: {ids}',
        'log.noClaimedTasks': 'No claimed tasks, getting available task list...',
        'log.taskClaimed': '✅ Claimed task: {title} (Task ID: {id})',
        'log.taskExecuting': '🔄 Executing task: {title}',
        'log.taskCompleted': '🎉 Task completed: {title}',
        'log.taskReward': '💰 Earned reward: {reward} ETH',
        'log.noAvailableTasks': '📭 No available tasks',
        'log.noSuitableTasks': '🔍 No suitable tasks found',
        'log.workFailed': '❌ Work cycle execution failed',
        'log.agentStarted': 'AI Agent started working',
        'log.autoWorkStarted': 'Auto work mode started',
        'log.autoWorkStopped': 'Auto work mode stopped',
        'log.walletConnected': 'Wallet connected successfully: {address}',
        'log.addressCopied': 'Address copied to clipboard',
        'log.loadFailed': 'Failed to load data, please check network connection'
    },
    
    // 获取翻译文本
    t(key, params = {}) {
        const translation = this[this.currentLanguage][key] || key;
        return translation.replace(/\{(\w+)\}/g, (match, param) => {
            return params[param] || match;
        });
    },
    
    // 切换语言
    setLanguage(lang) {
        this.currentLanguage = lang;
        this.updatePageLanguage();
        localStorage.setItem('flowai_language', lang);
        
        // 重新加载任务、网络信息和已认领任务显示以更新语言
        if (window.flowAIApp) {
            window.flowAIApp.loadTasks();
            window.flowAIApp.loadNetworkInfo();
            window.flowAIApp.updateClaimedTasksDisplay();
            window.flowAIApp.updateWalletDisplay(); // 更新钱包显示状态
        }
    },
    
    // 更新页面语言
    updatePageLanguage() {
        // 更新所有带有data-i18n属性的元素
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            if (element.tagName === 'INPUT' && element.type === 'placeholder') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // 更新语言切换按钮
        const langToggle = document.getElementById('languageToggle');
        if (langToggle) {
            const span = langToggle.querySelector('span');
            if (span) {
                span.textContent = this.currentLanguage === 'zh' ? 'EN' : '中文';
            }
        }
    },
    
    // 初始化
    init() {
        // 从localStorage恢复语言设置
        const savedLanguage = localStorage.getItem('flowai_language');
        if (savedLanguage && (savedLanguage === 'zh' || savedLanguage === 'en')) {
            this.currentLanguage = savedLanguage;
        }
        
        // 更新页面语言
        this.updatePageLanguage();
        
        // 绑定语言切换事件
        const langToggle = document.getElementById('languageToggle');
        if (langToggle) {
            langToggle.addEventListener('click', () => {
                const newLang = this.currentLanguage === 'zh' ? 'en' : 'zh';
                this.setLanguage(newLang);
            });
        }
    }
};

// 导出i18n对象
window.i18n = i18n; 