# Lychee-AI-Guard-DSS 🛡️

**基于边缘计算与人在回路 (HITL) 的农业专家决策支持系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stack: YOLOv8 + Flask + WeChatMP](https://img.shields.io/badge/Stack-YOLOv8%20%2B%20Flask%20%2B%20WeChatMP-green)](https://github.com/ultralytics/ultralytics)

## 📖 项目背景

在热带农业（尤其是荔枝种植）中，精准识别虫害是决定收成的关键。然而，单纯依赖边缘端轻量化深度学习模型（如 YOLO）存在以下痛点：
1. **高置信度幻觉**：在强光、阴影或幼虫特写场景下，模型可能以极高置信度将完全不同的物种逻辑错误归类（如将白色"蒂蛀虫"幼虫识别为棕色"荔枝蝽"成虫）。
2. **算力成本压力**：依赖云端大模型 API 会产生持续的 Token 费用，且受果园网络覆盖限制。

本系统通过**边缘计算(Local-First)**与**人在回路(Human-in-the-Loop)**的设计范式，在保证 0 Token 成本的前提下，利用物理规则网关彻底解决了上述识别顽疾。

---

## 🏗️ 系统架构：感知-网关-协同

本系统不仅仅是一个检测模型，而是一个三层防御体系：

1.  **感知层 (Perception Layer)**:
    *   部署经过针对性训练的 **YOLOv8** 模型，负责实时对象检测。
2.  **网关层 (Physical Gateway - "Sniper Interceptor")**:
    *   内置 **OpenCV HSV 视觉狙击手**。针对特定易混淆标签（如荔枝蝽），在 ROI 区域执行光谱分析。强制拦截"体色苍白"的误判逻辑并自动纠错。
3.  **协同层 (Collaborative HITL Layer)**:
    *   **动态路由机制**：针对低置信度（<80%）或易混淆类别，系统自动关闭“确诊”模式，优雅降级为“专家会诊”UI。
    *   **适老化交互**：44rpx 特大字号设计，专为高龄果农优化。

---

## 🛠️ 技术栈

*   **后端**: Python / Flask (轻量化高性能接口)
*   **算法**: Ultralytics YOLOv8 (目标检测) + OpenCV (色彩网关拦截)
*   **存储**: SQLite3 (本地数据飞轮)
*   **前端**: 微信小程序 (适老化 UI 设计)
*   **部署**: PM2 (生产环境进程守护)

---

## 🚀 演进史：从模型到工程

*   **Phase 1 (MVP)**: 纯 YOLO 模型部署。发现物理特征极度不稳定的“指白为黑”现象。
*   **Phase 2 (Hard Rules)**: 引入 OpenCV 几何校验。发现硬编码阈值在多变光照下过拟合，产生误杀。
*   **Phase 3 (Ultimate DSS)**: 落地 **HITL 动态路由**。引入“多选项会诊”应对非确定性环境，建立 SQLite RLHF 闭环，实现数据导向的系统自愈。

---

## 📝 简历亮点 (STAR 法则)

*   **架构重构**: 针对 Edge AI 高置信度幻觉，设计并实现了一套基于 OpenCV ROI 探测的混合式网关架构，在 0 Token 成本下将核心病害误判率降低了 XX%，显著提升了系统鲁棒性。
*   **产品容错**: 设计了“人在回路”专家决策流，实现动态置信度路由，在模型把握度不足时通过“多候选 UI”引导农户参与决策，解决了算法“一刀切”导致的农药误配风险。
*   **数据飞轮**: 构建了基于 SQLite 的本地记录与反馈闭环，捕获真实果园场景下的环境噪声数据，为后续模型 RLHF（基于人类反馈的强化学习）提供了高质量的真实样本库。

---

## 🏗️ 快速启动

1. 克隆代码库。
2. 运行 `pip install -r requirements.txt`。
3. 确保 `best.pt` 位于根目录，执行 `pm2 start app.py`。
4. 微信小程序指向本地 cpolar 或局域网端点。

---

*“懂算法的局限性，更懂如何用工程抵消局限性。”* 🦞
