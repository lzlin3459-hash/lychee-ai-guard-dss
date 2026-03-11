import gradio as gr
from ultralytics import YOLO
from PIL import Image
import numpy as np

# 1. 唤醒神医 (V3.0 终极权重)
model = YOLO('best.pt')

# 2. 官方花名册与建议库
DISEASE_NAMES = ['荔枝蝽', '荔枝蒂蛀虫', '荔枝霜疫霉病', '荔枝炭疽病', '荔枝瘿螨']
TREATMENT_DB = {
    '荔枝蝽': "● **物理防治**: 人工捕杀成虫。 ● **生物防治**: 释放平腹小蜂寄生。 ● **化学防治**: 若虫期喷施高效氯氰菊酯。",
    '荔枝蒂蛀虫': "● **农业防治**: 及时清除地面落果并深埋。 ● **物理防治**: 悬挂频振式杀虫灯。 ● **化学防治**: 成虫羽化高峰期喷药。",
    '荔枝霜疫霉病': "● **农业防治**: 注意果园排渍降湿，保持通风。 ● **化学防治**: 发病初期喷施甲霜灵、代森锰锌或施保克。",
    '荔枝炭疽病': "● **农业防治**: 剪除并烧毁病虫枝叶。 ● **化学防治**: 新梢和开花期，交替喷施百菌清或甲基硫菌灵。",
    '荔枝瘿螨': "● **农业防治**: 结合冬季清园剪除被害枝。 ● **化学防治**: 在春梢期和开花前，喷洒阿维菌素等杀螨剂。"
}

def clinical_diagnose(input_img, conf_val):
    if input_img is None: return None, "### 🩺 等待看诊...\n请上传照片。"
    
    # 🌟 保持 V3.1.7 的色彩稳定性
    img_pil = Image.fromarray(input_img).convert('RGB')
    results = model.predict(source=img_pil, conf=conf_val)
    
    # 生成结果图并校正色彩
    res_img_array = results[0].plot()
    res_img_rgb = Image.fromarray(res_img_array[..., ::-1]) 
    
    # 🌟 找回专家报告逻辑
    report = "## 🔬 专家临床诊断报告\n\n"
    detected_list = []

    if len(results[0].boxes) > 0:
        report += "### **一、诊断结果**\n"
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            name = DISEASE_NAMES[cls_id]
            score = float(box.conf[0])
            if name not in detected_list:
                detected_list.append(name)
            report += f"* **{name}** (置信度: {score:.2f}) {'✅' if score > 0.4 else '⚠️ 疑似'}\n"
        
        report += "\n### **二、实际防治建议**\n"
        for name in detected_list:
            suggestion = TREATMENT_DB.get(name, "建议联系当地农技推广中心。")
            report += f"针对 **{name}** 的防治方案：\n> {suggestion}\n\n"
    else:
        report += "**诊断结论**: 当前自信度门槛下未发现病害。若肉眼可见异常，请尝试**降低**自信度滑块。"
    
    report += "\n---\n*💡 提示: 本内容由 AI 辅助生成，仅供参考。重大决策请咨询专业农技人员。*"
    
    return res_img_rgb, report

# 3. 现代化临床布局
with gr.Blocks(title="荔枝卫士 V3.1.8", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🍎 荔枝 AI 卫士 - 临床全科诊疗系统")
    gr.Markdown("当前版本: V3.1.8 (集色彩校正、高精识别、防治建议于一体)")
    
    with gr.Row():
        with gr.Column(scale=1):
            img_in = gr.Image(label="1. 请上传荔枝照片")
            slider = gr.Slider(0.01, 1.0, value=0.15, label="2. AI 自信度门槛")
            btn = gr.Button("🔍 开始专家会诊", variant="primary")
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.TabItem("诊断结果图"):
                    img_out = gr.Image(label="诊断结果图")
                with gr.TabItem("临床报告单"):
                    text_out = gr.Markdown(label="专家建议报告")
            
    # 绑定事件
    btn.click(clinical_diagnose, [img_in, slider], [img_out, text_out])

if __name__ == "__main__":
    app.launch()