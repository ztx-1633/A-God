#!/usr/bin/env python3
"""
更新支付宝收款码
直接将用户提供的图片保存到static/images目录中
"""

import os
import requests
from PIL import Image
from io import BytesIO

# 确保static/images目录存在
images_dir = os.path.join(os.path.dirname(__file__), '炒股知识库', 'static', 'images')
os.makedirs(images_dir, exist_ok=True)

# 支付宝收款码图片URL
# 注意：这里需要替换为实际的图片URL
alipay_qr_url = "https://example.com/alipay_qr.jpg"

# 保存图片的路径
alipay_qr_path = os.path.join(images_dir, 'alipay.jpg')

try:
    # 下载图片
    response = requests.get(alipay_qr_url)
    response.raise_for_status()
    
    # 打开图片
    image = Image.open(BytesIO(response.content))
    
    # 保存图片
    image.save(alipay_qr_path, 'JPEG')
    
    print(f"支付宝收款码已成功更新到: {alipay_qr_path}")
except Exception as e:
    print(f"更新支付宝收款码失败: {e}")
