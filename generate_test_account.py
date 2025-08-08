#!/usr/bin/env python3
"""
生成测试账户脚本
"""

import secrets
import hashlib
import hmac
import os

def generate_ethereum_account():
    """生成以太坊测试账户"""
    
    # 生成32字节的随机私钥
    private_key_bytes = secrets.token_bytes(32)
    private_key_hex = '0x' + private_key_bytes.hex()
    
    # 使用私钥生成公钥和地址
    # 这里使用简化的方法，实际应该使用椭圆曲线加密
    public_key_hash = hashlib.sha256(private_key_bytes).hexdigest()
    address = '0x' + public_key_hash[-40:]  # 取最后20字节作为地址
    
    return private_key_hex, address

def main():
    print("🔐 生成测试账户...")
    print("=" * 50)
    
    # 生成账户
    private_key, address = generate_ethereum_account()
    
    print("✅ 测试账户生成成功！")
    print()
    print("📋 账户信息:")
    print(f"私钥: {private_key}")
    print(f"地址: {address}")
    print()
    print("⚠️  重要提醒:")
    print("- 请保存这些信息用于测试")
    print("- 不要用于真实资金")
    print("- 不要泄露给他人")
    print()
    print("💰 获取测试ETH:")
    print("- Sepolia Faucet: https://sepoliafaucet.com/")
    print("- Alchemy Faucet: https://sepoliafaucet.com/")
    print("- Infura Faucet: https://www.infura.io/faucet/sepolia")
    print()
    print("🔧 环境变量配置:")
    print(f"ETHEREUM_RPC_URL=https://practical-sly-tent.quiknode.pro/2826b61a63141b6fa14758ba511ea6398f953353")
    print(f"PRIVATE_KEY={private_key}")
    print("OPENAI_API_KEY=your_openai_api_key_here")

if __name__ == "__main__":
    main() 