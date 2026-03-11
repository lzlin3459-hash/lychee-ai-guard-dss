import requests
import os
import time

# ================= 架构师配置区 =================
# 咱们的 5 大核心考点
TARGET_BUGS = ['荔枝蝽', '荔枝蒂蛀虫', '荔枝霜疫霉病', '荔枝炭疽病', '荔枝瘿螨']
# 每种抓取数量（抓150张，方便你大浪淘沙选出最精品的50张）
FETCH_NUM = 150  
# 原始仓库文件夹名字
SAVE_DIR = 'Lychee_Dataset_Raw' 
# ===============================================

def fetch_images(keyword, max_num, base_dir):
    """核心抓取引擎：直连百度图片接口"""
    # 伪装成正常的浏览器访问
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    url = 'https://image.baidu.com/search/acjson'
    
    # 自动为每种病虫害建立专属文件夹
    folder_path = os.path.join(base_dir, keyword)
    os.makedirs(folder_path, exist_ok=True)
        
    downloaded = 0
    page = 0
    
    print(f"\n🚀 目标锁定: 【{keyword}】，开始执行抓取...")
    
    while downloaded < max_num:
        # 构造请求参数，模仿瀑布流下滑
        params = {
            'tn': 'resultjson_com', 'ipn': 'rj', 'word': keyword, 'queryWord': keyword,
            'pn': page * 30, 'rn': '30', 'ie': 'utf-8', 'oe': 'utf-8'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            # 如果没数据了就提前结束
            if not data.get('data'):
                print(f"⚠️ {keyword} 的图片已到底，停止抓取。")
                break
            
            for item in data['data']:
                if downloaded >= max_num:
                    break
                
                # 提取图片真实链接
                if item.get('thumbURL'):
                    img_url = item['thumbURL']
                    try:
                        # 下载图片
                        img_res = requests.get(img_url, headers=headers, timeout=5)
                        file_name = f"{keyword}_{downloaded + 1:03d}.jpg"
                        file_path = os.path.join(folder_path, file_name)
                        
                        with open(file_path, 'wb') as f:
                            f.write(img_res.content)
                            
                        downloaded += 1
                        print(f"  📦 成功入库: {file_name}")
                    except:
                        continue # 遇到死链接直接跳过，绝不卡死
                        
        except Exception as e:
            print(f"❌ 获取列表遇到波动，正在重试...")
            
        page += 1
        time.sleep(1) # 架构师的优雅：停顿1秒，防止被百度拉黑
        
    print(f"✅ 【{keyword}】任务完成！总计收入库中 {downloaded} 张。")

if __name__ == '__main__':
    print("🕷️ 荔枝 AI 卫士 - 全自动爬虫流水线启动！")
    # 创建总仓库
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # 挨个点名抓取
    for bug in TARGET_BUGS:
        fetch_images(bug, FETCH_NUM, SAVE_DIR)
        
    print(f"\n🎉 报告总指挥：所有原石已全部采集完毕！请前往 {SAVE_DIR} 文件夹验收！")