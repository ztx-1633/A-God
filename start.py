#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股股市分析预测软件 - 根目录启动脚本
自动切换到正确目录并启动系统
"""

import os
import sys
from pathlib import Path

def main():
    # 检查命令行参数
    skip_deps = False
    if len(sys.argv) > 1 and sys.argv[1] == '--skip-deps':
        skip_deps = True
        print("⚠️  跳过依赖检查，直接启动...")
    
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    project_dir = current_dir / "炒股知识库"
    
    # 检查项目目录是否存在
    if not project_dir.exists():
        print("❌ 错误：找不到'炒股知识库'目录")
        print(f"当前目录：{current_dir}")
        print("请确保项目结构正确")
        return
    
    # 切换到项目目录
    os.chdir(project_dir)
    print(f"📁 切换到项目目录：{project_dir}")
    
    # 检查run.py是否存在
    run_script = project_dir / "run.py"
    if not run_script.exists():
        print("❌ 错误：找不到run.py文件")
        return
    
    # 导入并运行主程序
    try:
        sys.path.insert(0, str(project_dir))
        
        print("🚀 启动A股智能分析平台...")
        print("="*50)
        
        # 导入并运行run.py的main函数
        import importlib.util
        spec = importlib.util.spec_from_file_location("run", run_script)
        run_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_module)
        
        # 根据参数决定调用方式
        if skip_deps:
            # 直接启动Web应用，跳过检查
            if hasattr(run_module, 'start_web_app'):
                run_module.start_web_app()
            else:
                # 如果没有start_web_app函数，直接运行app.py
                try:
                    from app import create_app
                    app = create_app()
                    print("🚀 A股智能分析平台启动成功！")
                    print("📊 访问地址: http://localhost:5000")
                    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
                except Exception as e:
                    print(f"直接启动失败: {e}")
        else:
            # 调用main函数
            if hasattr(run_module, 'main'):
                run_module.main()
            else:
                print("❌ 错误：run.py中没有找到main函数")
            
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        print("请检查依赖是否已正确安装")
        print("运行命令：pip install -r requirements.txt")

if __name__ == '__main__':
    main()