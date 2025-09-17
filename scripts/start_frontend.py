#!/usr/bin/env python3
"""
前端开发服务器启动脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    """主函数"""
    print("=" * 50)
    print("CTP Quote App Frontend Startup Script")
    print("=" * 50)
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    frontend_dir = project_root / "frontend"
    
    # 检查Node.js环境
    if not shutil.which("node"):
        print("❌ Node.js is not installed")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    if not shutil.which("npm"):
        print("❌ npm is not installed")
        print("Please install npm (usually comes with Node.js)")
        sys.exit(1)
    
    # 进入前端目录
    os.chdir(frontend_dir)
    print(f"📁 Working directory: {frontend_dir}")
    
    # 检查package.json
    if not (frontend_dir / "package.json").exists():
        print("❌ package.json not found")
        print("Please make sure you're in the correct frontend directory")
        sys.exit(1)
    
    # 检查node_modules
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)
    
    # 启动开发服务器
    print("🚀 Starting frontend development server...")
    print("=" * 50)
    
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 添加shutil导入
    import shutil
    main()
