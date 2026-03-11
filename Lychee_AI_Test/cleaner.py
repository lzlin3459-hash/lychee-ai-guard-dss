import cv2
import os
import numpy as np
from PIL import Image

# 1. 设定咱们的原始大仓库路径
dataset_dir = "Lychee_Dataset_Raw"

# 2. 设定“清晰度及格线”（数字越大，要求越严，一般 100 是个好起点）
blur_threshold = 100  

print("🤖 质检员已上线，开始全自动大扫除...")
deleted_count = 0

# 3. 让代码自动翻遍仓库里的每一个文件夹和每一张图片
for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        file_path = os.path.join(root, file)
        
        # --- 第一道关卡：查杀“坏死文件” ---
        try:
            img = Image.open(file_path)
            img.verify() # 验证文件是不是真正的图片
        except Exception:
            os.remove(file_path)
            print(f"🗑️ 销毁损坏文件: {file}")
            deleted_count += 1
            continue

        # --- 第二道关卡：查杀“重度模糊废片” ---
        try:
            # 架构师魔法：用 numpy 读取，完美解决 Windows 系统下中文文件夹报错的千古难题！
            cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
            
            if cv_img is None:
                continue
                
            # 将图片转换成黑白灰度图，方便电脑计算边缘
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            # 核心算法：计算图片的拉普拉斯方差（方差越小，边缘越模糊）
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 如果清晰度得分低于及格线，直接无情删除！
            if fm < blur_threshold:
                os.remove(file_path)
                print(f"👓 销毁模糊废片: {file} (清晰度得分仅为: {fm:.1f})")
                deleted_count += 1
                
        except Exception as e:
            pass

print(f"\n🎉 大扫除完美结束！总共为你无情销毁了 {deleted_count} 张垃圾废片！")