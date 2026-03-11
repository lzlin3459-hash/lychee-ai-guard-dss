from ultralytics import YOLO

# 1. 架构师指令：请出咱们的 V1.0 目标检测版超级卫士
print("🩺 正在唤醒 V1.0 目标检测版『荔枝 AI 卫士』...")
model = YOLO('best.pt')  # 确保新下载的 best.pt 就在旁边

# 2. 准备病例：还记得上次那张导致翻车的“广角大树照片”吗？就用它！
# ⚠️ 注意：填入你真实的图片路径，记得保留前面的小写 r
test_image = "bug_test.jpg" 

print(f"\n🔍 正在开启『火眼金睛』全景扫描：{test_image}")

# 3. 开始扫描！(save=True 这个魔法指令会让 AI 自动保存画好框的结果图)
results = model.predict(source=test_image, save=True, conf=0.1)

# 4. 输出诊断报告地址
print("\n================ 📝 最终诊断报告 ================")
print("✅ 扫描完成！AI 已经在图片上精准圈出了可疑病斑。")
print(f"👉 请立刻前往这个文件夹查看『画框结果图』：{results[0].save_dir}")
print("==================================================")