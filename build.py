#!/usr/bin/env python3
"""
项目打包脚本
使用PyInstaller将项目打包为可执行文件
"""

import os
import shutil
import subprocess
import sys
import platform

class BuildManager:
    """构建管理类"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.project_root, 'dist')
        self.build_dir = os.path.join(self.project_root, 'build')
        self.main_script = os.path.join(self.project_root, '炒股知识库', 'run.py')
    
    def clean_build(self):
        """清理构建目录"""
        print("清理构建目录...")
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        print("构建目录清理完成")
    
    def install_dependencies(self):
        """安装依赖"""
        print("安装依赖...")
        requirements_file = os.path.join(self.project_root, '炒股知识库', 'requirements.txt')
        if os.path.exists(requirements_file):
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_file], check=True)
        else:
            print("requirements.txt文件不存在，跳过依赖安装")
        print("依赖安装完成")
    
    def build_executable(self):
        """构建可执行文件"""
        print("构建可执行文件...")
        
        # 构建命令
        build_command = [
            'pyinstaller',
            '--onefile',
            '--name', 'stock_analysis_platform',
            '--distpath', self.output_dir,
            '--workpath', self.build_dir,
            '--noconsole',  # 无控制台窗口
            '--add-data', f'{os.path.join(self.project_root, "炒股知识库", "templates")};templates',
            '--add-data', f'{os.path.join(self.project_root, "炒股知识库", "static")};static',
            '--add-data', f'{os.path.join(self.project_root, "炒股知识库", "legal")};legal',
            '--hidden-import', 'flask',
            '--hidden-import', 'flask_cors',
            '--hidden-import', 'pandas',
            '--hidden-import', 'numpy',
            '--hidden-import', 'cryptography',
            '--hidden-import', 'sqlite3',
            '--hidden-import', 'hashlib',
            '--hidden-import', 'hmac',
            '--hidden-import', 'platform',
            '--hidden-import', 'ctypes',
            self.main_script
        ]
        
        # 执行构建命令
        try:
            subprocess.run(build_command, check=True)
            print("可执行文件构建完成")
        except subprocess.CalledProcessError as e:
            print(f"构建失败: {e}")
            return False
        
        return True
    
    def create_startup_script(self):
        """创建启动脚本"""
        print("创建启动脚本...")
        
        if platform.system() == 'Windows':
            startup_script = os.path.join(self.output_dir, 'start.bat')
            with open(startup_script, 'w', encoding='utf-8') as f:
                f.write('@echo off\n')
                f.write('echo 启动A股智能分析平台...\n')
                f.write('echo 正在检查环境...\n')
                f.write('stock_analysis_platform.exe\n')
                f.write('pause\n')
        else:
            startup_script = os.path.join(self.output_dir, 'start.sh')
            with open(startup_script, 'w', encoding='utf-8') as f:
                f.write('#!/bin/bash\n')
                f.write('echo "启动A股智能分析平台..."\n')
                f.write('echo "正在检查环境..."\n')
                f.write('./stock_analysis_platform\n')
            os.chmod(startup_script, 0o755)
        
        print("启动脚本创建完成")
    
    def copy_config_files(self):
        """复制配置文件"""
        print("复制配置文件...")
        
        # 复制数据库文件
        db_file = os.path.join(self.project_root, 'users.db')
        if os.path.exists(db_file):
            shutil.copy(db_file, self.output_dir)
        
        # 复制其他必要文件
        config_file = os.path.join(self.project_root, '炒股知识库', 'config.py')
        if os.path.exists(config_file):
            shutil.copy(config_file, self.output_dir)
        
        print("配置文件复制完成")
    
    def run(self):
        """运行构建流程"""
        print("开始构建项目...")
        
        # 清理构建目录
        self.clean_build()
        
        # 安装依赖
        self.install_dependencies()
        
        # 构建可执行文件
        if not self.build_executable():
            return False
        
        # 创建启动脚本
        self.create_startup_script()
        
        # 复制配置文件
        self.copy_config_files()
        
        print("构建完成！")
        print(f"可执行文件位置: {self.output_dir}")
        print("请运行 start.bat (Windows) 或 start.sh (Linux/Mac) 启动应用")
        
        return True

if __name__ == '__main__':
    build_manager = BuildManager()
    build_manager.run()
