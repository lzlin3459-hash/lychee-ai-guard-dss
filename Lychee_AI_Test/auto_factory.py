import os
import sys

# 架构师小妙招：强迫程序从当前环境找包
try:
    import pandas as pd
    from ultralytics import YOLO
except ImportError:
    print("❌ 依然找不到 pandas，请确保你选对了 VS Code 右下角的 Python 环境！")
    sys.exit()

def run_diagnosis():
    model_path = 'best.pt'
    excel_in = 'data.xlsx'
    
    if not os.path.exists(model_path):
        print("❌ 错误：没找到 best.pt！")
        return
    
    if not os.path.exists(excel_in):
        print("❌ 错误：没找到登记表 data.xlsx，请先运行 indexer.py！")
        return

    model = YOLO(model_path)
    df = pd.read_excel(excel_in)
    
    print("🩺 AI 正在全力诊断中...")
    results = []
    for path in df['图片路径']:
        if os.path.exists(path):
            res = model.predict(path, conf=0.4, verbose=False)
            label = res[0].names[int(res[0].boxes.cls[0])] if len(res[0].boxes) > 0 else "健康"
            results.append(label)
        else:
            results.append("图片缺失")
            
    df['AI 诊断结论'] = results
    df.to_excel('lychee_diagnostic_report.xlsx', index=False)
    print("✅ 诊断报告已出炉！")

if __name__ == "__main__":
    run_diagnosis()