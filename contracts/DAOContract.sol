// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DAOContract is Ownable, ReentrancyGuard {
    struct Proposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        bool canceled;
        mapping(address => bool) hasVoted;
        mapping(address => bool) support;
    }
    
    struct Member {
        address addr;
        uint256 votingPower;
        bool isActive;
        uint256 joinedAt;
    }
    
    IERC20 public governanceToken;
    mapping(uint256 => Proposal) public proposals;
    mapping(address => Member) public members;
    
    uint256 public proposalCounter;
    uint256 public quorumVotes;
    uint256 public votingPeriod;
    uint256 public proposalThreshold;
    
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string title);
    event VoteCast(address indexed voter, uint256 indexed proposalId, bool support, uint256 votes);
    event ProposalExecuted(uint256 indexed proposalId);
    event MemberAdded(address indexed member, uint256 votingPower);
    
    constructor(address _governanceToken) {
        governanceToken = IERC20(_governanceToken);
        quorumVotes = 1000 * 10**18; // 1000 tokens
        votingPeriod = 3 days;
        proposalThreshold = 100 * 10**18; // 100 tokens
    }
    
    modifier onlyMember() {
        require(members[msg.sender].isActive, "Not a member");
        _;
    }
    
    modifier proposalExists(uint256 proposalId) {
        require(proposals[proposalId].id != 0, "Proposal does not exist");
        _;
    }
    
    modifier proposalActive(uint256 proposalId) {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.startTime, "Proposal not started");
        require(block.timestamp <= proposal.endTime, "Proposal ended");
        require(!proposal.executed, "Proposal already executed");
        require(!proposal.canceled, "Proposal canceled");
        _;
    }
    
    function createProposal(
        string memory title,
        string memory description
    ) external onlyMember {
        require(governanceToken.balanceOf(msg.sender) >= proposalThreshold, "Insufficient tokens for proposal");
        
        proposalCounter++;
        Proposal storage proposal = proposals[proposalCounter];
        proposal.id = proposalCounter;
        proposal.proposer = msg.sender;
        proposal.title = title;
        proposal.description = description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        proposal.executed = false;
        proposal.canceled = false;
        
        emit ProposalCreated(proposalCounter, msg.sender, title);
    }
    
    function castVote(uint256 proposalId, bool support) external onlyMember proposalExists(proposalId) proposalActive(proposalId) {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.hasVoted[msg.sender], "Already voted");
        
        uint256 votes = governanceToken.balanceOf(msg.sender);
        require(votes > 0, "No voting power");
        
        proposal.hasVoted[msg.sender] = true;
        proposal.support[msg.sender] = support;
        
        if (support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }
        
        emit VoteCast(msg.sender, proposalId, support, votes);
    }
    
    function executeProposal(uint256 proposalId) external onlyMember proposalExists(proposalId) {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp > proposal.endTime, "Proposal not ended");
        require(!proposal.executed, "Proposal already executed");
        require(!proposal.canceled, "Proposal canceled");
        require(proposal.forVotes + proposal.againstVotes >= quorumVotes, "Quorum not reached");
        require(proposal.forVotes > proposal.againstVotes, "Proposal not passed");
        
        proposal.executed = true;
        
        // 这里可以添加具体的执行逻辑
        // 例如：更新任务奖励、修改合约参数等
        
        emit ProposalExecuted(proposalId);
    }
    
    function addMember(address member, uint256 votingPower) external onlyOwner {
        require(!members[member].isActive, "Member already exists");
        
        members[member] = Member({
            addr: member,
            votingPower: votingPower,
            isActive: true,
            joinedAt: block.timestamp
        });
        
        emit MemberAdded(member, votingPower);
    }
    
    function getProposal(uint256 proposalId) external view returns (
        uint256 id,
        address proposer,
        string memory title,
        string memory description,
        uint256 forVotes,
        uint256 againstVotes,
        uint256 startTime,
        uint256 endTime,
        bool executed,
        bool canceled
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.id,
            proposal.proposer,
            proposal.title,
            proposal.description,
            proposal.forVotes,
            proposal.againstVotes,
            proposal.startTime,
            proposal.endTime,
            proposal.executed,
            proposal.canceled
        );
    }
    
    function getMember(address memberAddr) external view returns (Member memory) {
        return members[memberAddr];
    }
    
    function hasVoted(uint256 proposalId, address voter) external view returns (bool) {
        return proposals[proposalId].hasVoted[voter];
    }
    
    function getVoteSupport(uint256 proposalId, address voter) external view returns (bool) {
        return proposals[proposalId].support[voter];
    }
    
    function getProposalCount() external view returns (uint256) {
        return proposalCounter;
    }
    
    function getQuorumVotes() external view returns (uint256) {
        return quorumVotes;
    }
    
    function getVotingPeriod() external view returns (uint256) {
        return votingPeriod;
    }
    
    function getProposalThreshold() external view returns (uint256) {
        return proposalThreshold;
    }
} 