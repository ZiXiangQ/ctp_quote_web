#!/usr/bin/env python3
"""
CTP配置向导脚本
"""

import os
import sys
from pathlib import Path


def main():
    """主函数"""
    print("=" * 60)
    print("🔧 CTP Configuration Wizard")
    print("=" * 60)

    # 获取项目路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    backend_dir = project_root / "backend"
    env_file = backend_dir / ".env"

    print("📋 Current Configuration:")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            print(content)
    else:
        print("❌ .env file not found")
        return

    print("\n" + "=" * 60)
    print("🔧 CTP Account Configuration")
    print("=" * 60)

    # 获取用户输入
    print("\n📝 Please enter your CTP account information:")

    # 用户ID
    user_id = input("🔑 CTP User ID: ").strip()
    if not user_id:
        print("❌ User ID cannot be empty")
        return

    # 密码
    password = input("🔒 CTP Password: ").strip()
    if not password:
        print("❌ Password cannot be empty")
        return

    # 环境选择
    print("\n🌐 Environment Selection:")
    print("1. Simulation (模拟环境) - 用于测试")
    print("2. Production (生产环境) - 真实交易")

    while True:
        env_choice = input("Choose environment (1/2): ").strip()
        if env_choice == "1":
            is_sim = "true"
            break
        elif env_choice == "2":
            is_sim = "false"
            break
        else:
            print("❌ Please enter 1 or 2")

    # 更新配置文件
    print("\n📝 Updating configuration...")

    # 读取现有配置
    config_lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            config_lines = f.readlines()

    # 更新配置
    updated_lines = []
    for line in config_lines:
        if line.startswith('CTP_USER_ID='):
            updated_lines.append(f'CTP_USER_ID={user_id}\n')
        elif line.startswith('CTP_PASSWORD='):
            updated_lines.append(f'CTP_PASSWORD={password}\n')
        elif line.startswith('CTP_IS_SIM='):
            updated_lines.append(f'CTP_IS_SIM={is_sim}\n')
        elif line.startswith('CTP_USE_MOCK='):
            updated_lines.append('CTP_USE_MOCK=false\n')
        else:
            updated_lines.append(line)

    # 写入更新后的配置
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)

    print("✅ Configuration updated successfully!")

    # 显示更新后的配置
    print("\n📋 Updated Configuration:")
    print("=" * 40)
    with open(env_file, 'r') as f:
        print(f.read())

    print("\n🚀 Next Steps:")
    print("1. Start the server: python3 scripts/start_server.py")
    print("2. Check CTP connection status")
    print("3. Test market data subscription")

    print("\n⚠️  Important Notes:")
    print("- Make sure your CTP account is active")
    print("- Check if you have market data permissions")
    print("- Simulation environment is recommended for testing")
    print("- Production environment requires real trading permissions")

if __name__ == "__main__":
    main()
