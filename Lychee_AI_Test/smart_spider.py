import os
import cv2
import numpy as np
from icrawler.builtin import BingImageCrawler, BaiduImageCrawler

# ==========================================
# 第一部分：专家级采购清单配置
# ==========================================
expert_targets = {
    "荔枝霜疫霉病": "Peronophythora litchii 白色霉层 荔枝",
    "荔枝炭疽病": "Colletotrichum gloeosporioides 荔枝 叶片褐斑",
    "荔枝蒂蛀虫": "Conopomorpha sinensis 蛀果",
    "荔枝蝽蟓": "Tessaratoma papillosa litchi bug",
    "荔枝瘿螨": "Eriophyes litchii 荔枝毛毡病"
}

base_folder = "Lychee_Dataset_Raw"

def crawl_images():
    print("\n🚀 第一阶段：智能爬虫开始全网定向采集...")
    for target_name, search_keyword in expert_targets.items():
        print(f"\n🎯 正在搜寻：{target_name} (关键词: {search_keyword})")
        save_dir = os.path.join(base_folder, target_name)
        
        try:
            BingImageCrawler(storage={'root_dir': save_dir}).crawl(keyword=search_keyword, max_num=20, min_size=(400, 400))
            BaiduImageCrawler(storage={'root_dir': save_dir}).crawl(keyword=search_keyword, max_num=20, min_size=(400, 400))
        except Exception as e:
            print(f"⚠️ {target_name} 抓取遇阻，自动跳过。")

# ==========================================
# 第二部分：无情质检员清理逻辑 (修复中文路径版)
# ==========================================
def clean_images(blur_threshold=30.0): # 阈值调降为30，防止误杀
    print("\n🧹 第二阶段：质检员上线，开始全自动大扫除...")
    deleted_count = 0
    
    if not os.path.exists(base_folder):
        print("❌ 没找到图片仓库，清理取消。")
        return

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                # 【核心修复】：用 numpy 底层读取，完美解决中文路径识别问题！
                img_data = np.fromfile(file_path, dtype=np.uint8)
                img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                
                if img is None:
                    os.remove(file_path)
                    print(f"🗑️ 销毁损坏文件: {file}")
                    deleted_count += 1
                    continue
                
                # 灰度化处理并计算清晰度
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                focus_measure = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                # 如果清晰度太低，删除
                if focus_measure < blur_threshold:
                    os.remove(file_path)
                    print(f"👓 销毁模糊废片: {file} (清晰度: {focus_measure:.1f})")
                    deleted_count += 1
                    
            except Exception as e:
                # 遇到异常文件，删除
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except:
                    pass

    print(f"\n✨ 大扫除完美结束！总共为你无情销毁了 {deleted_count} 张垃圾废片，剩下的都是精华！")

if __name__ == "__main__":
    print("🌟 荔枝 AI 卫士：数据采集与清洗一体化程序启动！")
    crawl_images()
    clean_images()
    print("🏆 恭喜！高质量病害图片已准备就绪！")