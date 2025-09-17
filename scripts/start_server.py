#!/usr/bin/env python3
"""
CTP行情服务启动脚本
支持完整安装和快速启动两种模式
"""

import os
import platform
import shutil
import socket
import subprocess
import sys
from pathlib import Path


def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return '127.0.0.1'

def print_server_info():
    """打印服务器信息"""
    local_ip = get_local_ip()
    print("=" * 60)
    print("🚀 CTP Quote App Backend Server")
    print("=" * 60)
    print("📋 Configuration:")
    print("   Port: 5005")
    print("   Host: 0.0.0.0 (all interfaces)")
    print("   Mock Mode: True (using mock data)")
    print()
    print("🌐 Server IP Addresses:")
    print(f"   Local IP: {local_ip}")
    print("   Localhost: 127.0.0.1")
    print()
    print("🔗 Access URLs:")
    print(f"   Local:    http://127.0.0.1:5005")
    print(f"   Network:  http://{local_ip}:5005")
    print(f"   WebSocket: ws://{local_ip}:5005/socket.io/")
    print()

def check_python_environment():
    """检查Python环境"""
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    if not shutil.which(python_cmd):
        print("❌ Python3 is not installed")
        print("Please install Python 3.8 or higher")
        sys.exit(1)
    return python_cmd

def setup_virtual_environment(backend_dir, python_cmd):
    """设置虚拟环境"""
    venv_dir = backend_dir / "venv"  # 使用venv而不是.venv

    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([python_cmd, "-m", "venv", "venv"], check=True, cwd=backend_dir)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            sys.exit(1)

    # 确定虚拟环境中的Python和pip命令
    if platform.system() == "Windows":
        venv_python = str(venv_dir / "Scripts" / "python")
        venv_pip = str(venv_dir / "Scripts" / "pip")
    else:
        venv_python = str(venv_dir / "bin" / "python")
        venv_pip = str(venv_dir / "bin" / "pip")

    return venv_python, venv_pip

def install_dependencies(venv_python, venv_pip, backend_dir):
    """安装依赖"""
    print("🔧 Installing dependencies...")
    try:
        # 升级pip
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True, cwd=backend_dir)

        # 安装依赖
        subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True, cwd=backend_dir)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_config_file(backend_dir):
    """设置配置文件"""
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  .env file not found, creating from template...")
        try:
            env_example = backend_dir / "env.example"
            if env_example.exists():
                env_file.write_text(env_example.read_text())
                print("📝 .env file created from template")
            else:
                # 创建默认配置
                default_config = """# CTP配置
CTP_IS_SIM=true
CTP_USE_MOCK=true
CTP_USER_ID=
CTP_PASSWORD=

# Flask配置
SECRET_KEY=dev-secret-key
PORT=5005

# 日志配置
LOG_LEVEL=INFO
"""
                env_file.write_text(default_config)
                print("📝 Default .env file created")

            print("📝 Please edit .env file with your CTP credentials if needed")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            sys.exit(1)

def quick_start(backend_dir):
    """快速启动模式（假设环境已配置）"""
    print("🚀 Quick Start Mode")
    print("=" * 50)

    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv")
        print("Or use full setup mode")
        sys.exit(1)

    # 确定Python命令
    if platform.system() == "Windows":
        python_cmd = str(venv_dir / "Scripts" / "python")
    else:
        python_cmd = str(venv_dir / "bin" / "python")

    # 检查Python是否存在
    if not os.path.exists(python_cmd):
        print(f"❌ Python not found at: {python_cmd}")
        sys.exit(1)

    print(f"🐍 Using Python: {python_cmd}")
    return python_cmd

def full_setup(backend_dir):
    """完整安装模式"""
    print("🔧 Full Setup Mode")
    print("=" * 50)
    # 检查Python环境
    python_cmd = check_python_environment()
    # 设置虚拟环境
    venv_python, venv_pip = setup_virtual_environment(backend_dir, python_cmd)
    # 安装依赖
    install_dependencies(venv_python, venv_pip, backend_dir)
    # 设置配置文件
    setup_config_file(backend_dir)
    return venv_python

def main():
    """主函数"""
    # 检查命令行参数
    mode = "quick"  # 默认快速模式
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--full", "-f", "full"]:
            mode = "full"
        elif sys.argv[1] in ["--help", "-h", "help"]:
            print("Usage: python start_server.py [mode]")
            print("Modes:")
            print("  quick (default) - Quick start, assumes environment is set up")
            print("  full           - Full setup, creates venv and installs dependencies")
            print("  help           - Show this help message")
            sys.exit(0)

    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    backend_dir = project_root / "backend"

    # 进入后端目录
    os.chdir(backend_dir)
    print(f"📁 Working directory: {backend_dir}")

    # 根据模式选择启动方式
    if mode == "full":
        python_cmd = full_setup(backend_dir)
    else:
        python_cmd = quick_start(backend_dir)
    # 启动服务
    print("🚀 Starting CTP Quote Server...")
    print("=" * 60)
    # 显示服务器信息
    print_server_info()
    try:
        subprocess.run([python_cmd, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
