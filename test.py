import cv2
import numpy as np
import os

# 模板文件夹路径
template_folder = 'template'

# 加载模板图像并按需缩放
templates = {}
for filename in os.listdir(template_folder):
    if filename.endswith('.png'):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is not None:
            templates[filename] = template

# 初始化摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        print("无法捕获图像")
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 遍历所有模板
    for filename, template in templates.items():
        # 获取模板图像和视频帧的尺寸
        th, tw = template.shape
        fh, fw = gray.shape

        # 如果模板图像大于视频帧尺寸，则缩放模板图像
        if th > fh or tw > fw:
            scale_factor = min(fh / th, fw / tw)
            template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)
            th, tw = template.shape  # 更新模板图像的尺寸
        
        # 进行模板匹配
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 匹配阈值
        loc = np.where(res >= threshold)

        # 在所有匹配的位置上绘制边框
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + tw, pt[1] + th), (0, 255, 0), 2)
            print(f"Match found for template: {filename}")

    # 显示结果
    cv2.imshow('Frame', frame)

    # 如果按下'q'键，则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()

