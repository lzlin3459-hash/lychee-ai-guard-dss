import cv2
import os
import numpy as np
import random

# ================= 架构师 V4.6 配置区 =================
FOLDER_NAME = 'My_Lychee_Data_V3_Fixed' 
BOOST_FACTOR = 5 # 保持适度的增强倍数，防止特征稀释
# ======================================================

def cv_imread(file_path):
    return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)

def cv_imwrite(file_path, img):
    cv2.imencode('.jpg', img)[1].tofile(file_path)

def apply_smart_variety_filter(img):
    """
    V4.6 核心科技：带病灶保护机制的品种滤镜
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = cv2.split(hsv)
    
    # 🌟 核心突破：构建“病灶保护蒙版”
    # 炭疽病斑、虫洞通常是暗色（低亮度 v < 100）或灰褐色（低饱和度 s < 80）
    # 我们只对那些真正鲜亮、饱和的“健康果皮”进行颜色变换！
    skin_mask = (s > 80) & (v > 100)
    
    mode = random.choice(['feizixiao', 'heiye', 'baitangying', 'normal'])
    
    if mode == 'feizixiao':
        # 🟢 模拟‘妃子笑’：微调红色为青绿，力度减弱，防止变异
        target_mask = skin_mask & ((h > 160) | (h < 15))
        h[target_mask] = (h[target_mask] - 15) % 180  # 偏移量从 30 降为 15
        s[target_mask] = s[target_mask] * 0.85
    elif mode == 'heiye':
        # 🔴 模拟‘黑叶’：仅适度压暗果皮
        target_mask = skin_mask & ((h > 160) | (h < 15))
        v[target_mask] = v[target_mask] * 0.8 
    elif mode == 'baitangying':
        # 🍎 模拟‘白糖罂’：适度提亮
        v[skin_mask] = np.clip(v[skin_mask] * 1.1, 0, 255)
        s[skin_mask] = np.clip(s[skin_mask] * 1.1, 0, 255)
        
    return cv2.cvtColor(cv2.merge((h, s, v)).astype(np.uint8), cv2.COLOR_HSV2BGR)

def flip_bbox(bbox):
    cls, x, y, w, h = bbox
    return [cls, 1.0 - x, y, w, h]

def boost_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, FOLDER_NAME)
    img_dir = os.path.join(base_path, 'images')
    lbl_dir = os.path.join(base_path, 'labels')
    save_path = os.path.join(current_dir, 'My_Lychee_Data_V4_6_Ultimate')

    if not os.path.exists(img_dir):
        print(f"❌ 错误：找不到路径 {img_dir}")
        return

    os.makedirs(os.path.join(save_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(save_path, 'labels'), exist_ok=True)

    file_list = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))]
    print(f"🚀 V4.6 启动！正在执行带病灶保护的增强协议...")

    for filename in file_list:
        name_no_ext = os.path.splitext(filename)[0]
        img = cv_imread(os.path.join(img_dir, filename))
        lbl_path = os.path.join(lbl_dir, name_no_ext + '.txt')
        
        if img is None or not os.path.exists(lbl_path): continue

        with open(lbl_path, 'r', encoding='utf-8') as f:
            bboxes = [list(map(float, line.split())) for line in f.readlines()]

        # 1. 保存原图，确保 V3 的优秀基因 100% 传承
        cv_imwrite(os.path.join(save_path, 'images', filename), img)
        with open(os.path.join(save_path, 'labels', name_no_ext + '.txt'), 'w', encoding='utf-8') as f:
            for b in bboxes: f.write(f"{int(b[0])} {' '.join(map(str, b[1:]))}\n")

        # 2. 生成增强变体
        for i in range(BOOST_FACTOR):
            work_img = img.copy()
            work_bboxes = [b[:] for b in bboxes]
            
            # A. 智能品种滤镜 (降低触发概率到 30%，保留更多原貌)
            if random.random() > 0.7:
                work_img = apply_smart_variety_filter(work_img)
            
            # B. 轻度环境增强
            if random.random() > 0.6:
                val = random.randint(-30, 30)
                work_img = cv2.convertScaleAbs(work_img, alpha=1, beta=val)
            
            # C. 几何翻转
            if random.random() > 0.5:
                work_img = cv2.flip(work_img, 1)
                work_bboxes = [flip_bbox(b) for b in bboxes]

            new_name = f"{name_no_ext}_v46_{i}"
            cv_imwrite(os.path.join(save_path, 'images', f"{new_name}.jpg"), work_img)
            with open(os.path.join(save_path, 'labels', f"{new_name}.txt"), 'w', encoding='utf-8') as f:
                for b in work_bboxes:
                    f.write(f"{int(b[0])} {' '.join(map(str, b[1:]))}\n")

    print(f"✨ V4.6 炼金完毕！终极训练包已存入 My_Lychee_Data_V4_6_Ultimate！")

if __name__ == "__main__":
    boost_data()