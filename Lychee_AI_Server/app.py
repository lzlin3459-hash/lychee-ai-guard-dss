import os
import io
import json
import uuid
import datetime
import sqlite3
import numpy as np
import cv2
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

# --- 1. 环境自愈与数据库初始化 ---
os.makedirs('images', exist_ok=True)
def init_db():
    with sqlite3.connect('history.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history_logs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, img_path TEXT, 
                      final_name TEXT, conf REAL, intercepted INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS exception_logs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, img_path TEXT, 
                      name TEXT, conf REAL, reason TEXT)''')
        conn.commit()
init_db()

print("⏳ 正在加载 AI 视觉引擎...")
try:
    model = YOLO('best.pt')
    print("✅ 模型加载成功！荔枝 AI 卫士终极组合版已启动。")
except Exception as e:
    print(f"❌ 模型加载失败: {e}")

# --- 2. 核心字典库 (清洗了所有的 HTML 乱码字符) ---
DISEASE_DICT = {
    'stink_bug': {'name': '荔枝蝽', 'desc': '棕/褐色盾牌状成虫。', 'advice': '喷洒 4.5% 高效氯氰菊酯 1500 倍液。'},
    'lizhichun': {'name': '荔枝蝽', 'desc': '棕/褐色盾牌状成虫。', 'advice': '喷洒 4.5% 高效氯氰菊酯 1500 倍液。'},
    'borer': {'name': '蒂蛀虫', 'desc': '白/淡黄色软体幼虫。', 'advice': '羽化盛期喷洒 1.8% 阿维菌素乳油。'},
    'dizhuchong': {'name': '蒂蛀虫', 'desc': '白/淡黄色软体幼虫。', 'advice': '羽化盛期喷洒 1.8% 阿维菌素乳油。'},
    'frost_blight': {'name': '霜疫霉病', 'desc': '果皮表面白色霜状霉层。', 'advice': '喷洒 58% 甲霜灵·锰锌 600 倍液。'},
    'gall_mite': {'name': '荔枝瘿螨', 'desc': '叶片黄褐色毛绒凸起。', 'advice': '剪除病叶，喷洒 24% 螺螨酯悬浮剂。'},
    'anthracnose': {'name': '炭疽病', 'desc': '果实褐色凹陷病斑。', 'advice': '使用 10% 苯醚甲环唑 1500 倍液。'}
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "未接收到图片"})

        file = request.files['file']
        img_bytes = file.read()
        img_pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_cv2 = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        
        # 存图
        img_name = f"{uuid.uuid4().hex}.jpg"
        img_path = os.path.join('images', img_name)
        img_pil.save(img_path)

        # 预测
        results = model.predict(img_pil, conf=0.25)
        preds_list = json.loads(results[0].to_json())

        if not preds_list:
            return jsonify({"status": "success", "mode": "safe", "message": "✅ 未发现明显病虫害，请保持日常巡视。"})

        is_intercepted = 0
        raw_name = preds_list[0]['name'].lower().strip() # 强制清洗 Stink_Bug
        conf = round(preds_list[0]['confidence'] * 100, 1)

        # --- 3. 狙击手防线：专杀“指白为黑”的低级错误 ---
        if raw_name in ['stink_bug', 'lizhichun']:
            box = preds_list[0]['box']
            x1, y1, x2, y2 = int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2'])
            roi = img_cv2[y1:y2, x1:x2]
            if roi.size > 0:
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mean_s = np.mean(hsv_roi[:, :, 1])
                mean_v = np.mean(hsv_roi[:, :, 2])
                # 如果极其苍白明亮，一票否决
                if mean_s < 60 and mean_v > 120:
                    raw_name = 'borer'
                    conf = 99.9
                    is_intercepted = 1

        # --- 4. 组装候选列表与模式路由 ---
        candidates = []
        top1_info = DISEASE_DICT.get(raw_name, {'name': f'未知标签 ({raw_name})', 'desc': '尚未录入图谱', 'advice': '请人工协助。'})
        
        candidates.append({
            "name": top1_info['name'] + (" [底层防线纠错生效]" if is_intercepted else ""),
            "conf": conf,
            "desc": top1_info['desc'],
            "advice": top1_info['advice'],
            "raw_name": raw_name
        })

        # 判断是否进入会诊模式
        if conf < 80 or raw_name in ['stink_bug', 'lizhichun', 'borer', 'dizhuchong']:
            # 塞入备选项 (去掉 0% 的尴尬，强制不传 conf 或传 null)
            backup_key = 'borer' if raw_name in ['stink_bug', 'lizhichun'] else 'stink_bug'
            backup_info = DISEASE_DICT[backup_key]
            candidates.append({
                "name": backup_info['name'] + " (易混淆备选)",
                "conf": None, # 核心：不要传 0%，前端收到 null 就会显示需人工确认
                "desc": backup_info['desc'],
                "advice": backup_info['advice']
            })
            mode = "confirm"
        else:
            mode = "direct"

        # --- 5. 飞轮落盘 ---
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect('history.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO history_logs (time, img_path, final_name, conf, intercepted) VALUES (?, ?, ?, ?, ?)",
                      (now, img_path, raw_name, conf, is_intercepted))
            conn.commit()

        return jsonify({"status": "success", "mode": mode, "candidates": candidates})

    except Exception as e:
        return jsonify({"status": "error", "message": f"服务器内部开小差了: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)