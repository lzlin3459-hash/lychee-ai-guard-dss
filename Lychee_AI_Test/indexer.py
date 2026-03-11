import pandas as pd
import os

image_root = "Lychee_Dataset_Raw"
data_list = []

print("📦 正在清点仓库并生成登记表...")

# 自动扫描文件夹
if os.path.exists(image_root):
    for root, dirs, files in os.walk(image_root):
        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                full_path = os.path.join(root, file)
                label = os.path.basename(root) # 文件夹名就是病害名
                data_list.append({'图片路径': full_path, '原始标注': label})

    df = pd.DataFrame(data_list)
    df.to_excel('data.xlsx', index=False)
    print(f"✅ 登记完毕，共记录 {len(data_list)} 张图片。")
else:
    print("⚠️ 还没找到图片仓库，请先运行爬虫！")