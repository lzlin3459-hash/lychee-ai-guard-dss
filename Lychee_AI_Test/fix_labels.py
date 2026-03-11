import os

print("🧙‍♂️ 正在启动 V3.0 标签魔法修复阵...")

# ================= 架构师配置区 =================
# 1. 确保这个路径指向你解压出来的那个装满 250 个 txt 文件的文件夹！
# 假设你把 txt 都放在了桌面的 My_Lychee_Data_V3 里的 labels 文件夹下
LABEL_DIR = r'C:\Users\Lenovo\Desktop\My_Lychee_Data_V3\labels' 

# 2. 咱们的官方花名册与学号的映射关系（机器绝对不会认错）
CLASS_MAPPING = {
    '荔枝蝽': '0',
    '荔枝蒂蛀虫': '1',
    '荔枝霜疫霉病': '2',
    '荔枝炭疽病': '3',
    '荔枝瘿螨': '4'
}
# ===============================================

fixed_count = 0

# 遍历文件夹里的每一个 txt 文件
for filename in os.listdir(LABEL_DIR):
    if not filename.endswith('.txt') or filename == 'classes.txt':
        continue
        
    filepath = os.path.join(LABEL_DIR, filename)
    
    # 智能判断：根据文件名里的汉字，找出它应该对应的正确学号
    correct_id = '0' 
    for bug_name, bug_id in CLASS_MAPPING.items():
        if bug_name in filename:
            correct_id = bug_id
            break
            
    # 打开文件，读取里面的框数据
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    # 逐行修改：把开头的那个错误数字，替换成咱们刚才算出来的 correct_id
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0:
            parts[0] = correct_id  # 👈 核心魔法：强行篡改学号！
            new_lines.append(' '.join(parts) + '\n')
            
    # 把修改后的正确数据重新写回文件里
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    fixed_count += 1

print(f"🎉 魔法施展完毕！成功瞬间修复了 {fixed_count} 个文件的标签！再也不用看网页黑屏了！")