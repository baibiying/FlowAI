// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TaskContract is Ownable, ReentrancyGuard {
    struct Task {
        uint256 id;
        address publisher;
        string title;
        string description;
        uint256 reward;
        bool isCompleted;
        bool isClaimed;
        address worker;
        uint256 createdAt;
        uint256 deadline;
        string taskType;
        string requirements;
    }
    
    struct Worker {
        address addr;
        uint256 reputation;
        uint256 completedTasks;
        uint256 totalEarnings;
        bool isActive;
    }
    
    IERC20 public rewardToken;
    mapping(uint256 => Task) public tasks;
    mapping(address => Worker) public workers;
    mapping(address => uint256[]) public workerTasks;
    
    uint256 public taskCounter;
    uint256 public totalTasks;
    uint256 public totalRewards;
    
    event TaskCreated(uint256 indexed taskId, address indexed publisher, string title, uint256 reward);
    event TaskClaimed(uint256 indexed taskId, address indexed worker);
    event TaskCompleted(uint256 indexed taskId, address indexed worker, uint256 reward);
    event WorkerRegistered(address indexed worker);
    event RewardPaid(address indexed worker, uint256 amount);
    
    constructor(address _rewardToken) {
        rewardToken = IERC20(_rewardToken);
    }
    
    modifier taskExists(uint256 taskId) {
        require(tasks[taskId].id != 0, "Task does not exist");
        _;
    }
    
    modifier taskNotCompleted(uint256 taskId) {
        require(!tasks[taskId].isCompleted, "Task already completed");
        _;
    }
    
    modifier taskNotClaimed(uint256 taskId) {
        require(!tasks[taskId].isClaimed, "Task already claimed");
        _;
    }
    
    function createTask(
        string memory title,
        string memory description,
        uint256 reward,
        uint256 deadline,
        string memory taskType,
        string memory requirements
    ) external {
        require(reward > 0, "Reward must be greater than 0");
        require(deadline > block.timestamp, "Deadline must be in the future");
        
        taskCounter++;
        tasks[taskCounter] = Task({
            id: taskCounter,
            publisher: msg.sender,
            title: title,
            description: description,
            reward: reward,
            isCompleted: false,
            isClaimed: false,
            worker: address(0),
            createdAt: block.timestamp,
            deadline: deadline,
            taskType: taskType,
            requirements: requirements
        });
        
        totalTasks++;
        totalRewards += reward;
        
        emit TaskCreated(taskCounter, msg.sender, title, reward);
    }
    
    function claimTask(uint256 taskId) external taskExists(taskId) taskNotCompleted(taskId) taskNotClaimed(taskId) {
        Task storage task = tasks[taskId];
        require(block.timestamp <= task.deadline, "Task deadline passed");
        
        // 注册工人（如果还没有注册）
        if (!workers[msg.sender].isActive) {
            workers[msg.sender] = Worker({
                addr: msg.sender,
                reputation: 0,
                completedTasks: 0,
                totalEarnings: 0,
                isActive: true
            });
            emit WorkerRegistered(msg.sender);
        }
        
        task.isClaimed = true;
        task.worker = msg.sender;
        workerTasks[msg.sender].push(taskId);
        
        emit TaskClaimed(taskId, msg.sender);
    }
    
    function completeTask(uint256 taskId, string memory result) external taskExists(taskId) taskNotCompleted(taskId) {
        Task storage task = tasks[taskId];
        require(task.worker == msg.sender, "Only assigned worker can complete task");
        require(task.isClaimed, "Task not claimed");
        
        task.isCompleted = true;
        
        // 更新工人统计
        Worker storage worker = workers[msg.sender];
        worker.completedTasks++;
        worker.totalEarnings += task.reward;
        worker.reputation += 10; // 简单声誉系统
        
        // 转移奖励
        require(rewardToken.transfer(msg.sender, task.reward), "Reward transfer failed");
        
        emit TaskCompleted(taskId, msg.sender, task.reward);
        emit RewardPaid(msg.sender, task.reward);
    }
    
    function getTask(uint256 taskId) external view returns (Task memory) {
        return tasks[taskId];
    }
    
    function getWorker(address workerAddr) external view returns (Worker memory) {
        return workers[workerAddr];
    }
    
    function getWorkerTasks(address workerAddr) external view returns (uint256[] memory) {
        return workerTasks[workerAddr];
    }
    
    function getAvailableTasks() external view returns (uint256[] memory) {
        uint256[] memory availableTasks = new uint256[](taskCounter);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= taskCounter; i++) {
            if (!tasks[i].isClaimed && !tasks[i].isCompleted && block.timestamp <= tasks[i].deadline) {
                availableTasks[count] = i;
                count++;
            }
        }
        
        // 调整数组大小
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = availableTasks[i];
        }
        
        return result;
    }
    
    function getTaskCount() external view returns (uint256) {
        return taskCounter;
    }
    
    function getTotalRewards() external view returns (uint256) {
        return totalRewards;
    }
} 