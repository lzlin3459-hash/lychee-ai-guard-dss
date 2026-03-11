from icrawler.builtin import BingImageCrawler, BaiduImageCrawler
import os

# 1. 架构师的“专家级采购清单”
# 结合了拉丁学名与你查到的《科普中国》及权威机构的病理特征描述
expert_targets = {
    # 针对霜疫霉病，使用具体的症状词代替宽泛的病名
    "荔枝霜疫霉病_白色霉层": "Peronophythora litchii 白色霉层",
    "荔枝霜疫霉病_水渍状褐斑": "荔枝果实 水渍状褐斑",
    "荔枝霜疫霉病_花穗腐烂": "荔枝花穗 褐变腐烂",
    
    # 其他病害同样使用多维词汇组合
    "荔枝炭疽病_病斑": "Colletotrichum gloeosporioides 荔枝 叶片褐斑",
    "荔枝蒂蛀虫_受害果": "Conopomorpha sinensis 蛀果",
    "荔枝蝽蟓_成虫": "Tessaratoma papillosa litchi bug",
    "荔枝瘿螨_毛毡病": "Eriophyes litchii 荔枝毛毡病"
}

base_folder = "Lychee_Dataset_Raw"

print("🚀 荔枝 AI 卫士：专家级特征采集系统启动...")

for target_name, search_keyword in expert_targets.items():
    print(f"\n🎯 正在依据专家知识图谱搜寻：{target_name} (关键词: {search_keyword})")
    
    save_dir = os.path.join(base_folder, target_name.split('_')[0]) # 把同类病害放到一个大文件夹
    
    # 策略 A：使用 Bing 引擎获取带拉丁学名的国际学术及专业图片
    try:
        bing_crawler = BingImageCrawler(storage={'root_dir': save_dir})
        bing_crawler.crawl(keyword=search_keyword, max_num=30, min_size=(400, 400))
    except Exception as e:
        print(f"⚠️ Bing 抓取 {target_name} 遇阻，切换引擎...")
        
    # 策略 B：使用 Baidu 引擎获取国内如“百度百科”、“科普中国”的本地化图片
    try:
        baidu_crawler = BaiduImageCrawler(storage={'root_dir': save_dir})
        baidu_crawler.crawl(keyword=search_keyword, max_num=30, min_size=(400, 400))
    except Exception as e:
        print(f"⚠️ Baidu 抓取 {target_name} 遇阻...")

print("\n🎉 专家级采集完毕！请前往仓库检阅。")