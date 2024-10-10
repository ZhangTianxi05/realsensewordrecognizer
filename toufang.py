import cv2
import numpy as np
import os
from time import sleep
# 模板文件夹路径
template_folder = 'template'
flag=False
# 加载模板图像
templates = {}
for filename in os.listdir(template_folder):
    if filename.endswith('.png'):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is not None:
            templates[filename] = template

# 初始化摄像头
cap = cv2.VideoCapture(1)

# 设定多尺度匹配的缩放因子
scales = [0.1,0.2,0.3,0.4,0.5, 0.75, 1.0, 1.25, 1.5]

while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        print("无法捕获图像")
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 初始化最佳匹配结果
    best_match = None
    best_match_val = -1
    best_match_size = (0, 0)
    best_match_filename = None

    # 遍历所有模板和多尺度
    for filename, template in templates.items():
        for scale in scales:
            # 缩放模板图像
            resized_template = cv2.resize(template, None, fx=scale, fy=scale)
            th, tw = resized_template.shape
            
            # 如果模板图像大于视频帧，则跳过此尺度
            if th > gray.shape[0] or tw > gray.shape[1]:
                continue

            # 进行模板匹配
            res = cv2.matchTemplate(gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            # 更新最佳匹配结果
            if max_val > best_match_val:
                best_match_val = max_val
                best_match = max_loc
                best_match_size = resized_template.shape
                best_match_filename = filename[0]

    # 输出最佳匹配结果
    if best_match_val > 0.8:
        flag=True
        print(f"识别到模板: {best_match_filename} (置信度: {best_match_val})")
        recognized=best_match_filename
        # 计算最佳匹配的矩形框位置
        top_left = best_match
        bottom_right = (top_left[0] + best_match_size[1], top_left[1] + best_match_size[0])
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
    else:
        print("未识别到模板")

    # 显示结果
    cv2.imshow('Frame', frame)

    # 如果按下'q'键，则退出循环
    if flag==True or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()
'''
FashionStar Uart舵机 
> 设置舵机角度 <
--------------------------------------------------
- 作者: 阿凯
- Email: kyle.xing@fashionstar.com.hk
- 更新时间: 2020-12-5
--------------------------------------------------
'''
# 添加uservo.py的系统路径
import sys
sys.path.append("../src")
# 导入依赖
import time
import struct
import serial
from uservo import UartServoManager

# 参数配置
# 角度定义
SERVO_PORT_NAME =  'COM12'		# 舵机串口号
SERVO_BAUDRATE = 115200			# 舵机的波特率
SERVO_ID = 0					# 舵机的ID号
SERVO_HAS_MTURN_FUNC = False	# 舵机是否拥有多圈模式

# 初始化串口
uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
					 parity=serial.PARITY_NONE, stopbits=1,\
					 bytesize=8,timeout=0)
# 初始化舵机管理器
uservo = UartServoManager(uart, is_debug=True)

print("[单圈模式]设置舵机角度为90.0°")
uservo.set_servo_angle(SERVO_ID, 90, interval=0) # 设置舵机角度 极速模式
uservo.wait() # 等待舵机静止
print("-> {}".format(uservo.query_servo_angle(SERVO_ID)))

sleep(3)

print("[单圈模式]设置舵机角度为90.0°")
uservo.set_servo_angle(SERVO_ID, 1, interval=0) # 设置舵机角度 极速模式
uservo.wait() # 等待舵机静止
print("-> {}".format(uservo.query_servo_angle(SERVO_ID)))

cap = cv2.VideoCapture(0)

# 设定多尺度匹配的缩放因子

while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        print("无法捕获图像")
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 初始化最佳匹配结果
    best_match = None
    best_match_val = -1
    best_match_size = (0, 0)
    best_match_filename = None

    # 遍历所有模板和多尺度
    for filename, template in templates.items():
        for scale in scales:
            # 缩放模板图像
            resized_template = cv2.resize(template, None, fx=scale, fy=scale)
            th, tw = resized_template.shape
            
            # 如果模板图像大于视频帧，则跳过此尺度
            if th > gray.shape[0] or tw > gray.shape[1]:
                continue

            # 进行模板匹配
            res = cv2.matchTemplate(gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            # 更新最佳匹配结果
            if max_val > best_match_val:
                best_match_val = max_val
                best_match = max_loc
                best_match_size = resized_template.shape
                best_match_filename = filename[0]

    # 输出最佳匹配结果
    if best_match_val > 0.8:
        flag=True
        print(f"识别到模板: {best_match_filename} (置信度: {best_match_val})")
        # 计算最佳匹配的矩形框位置
        top_left = best_match
        bottom_right = (top_left[0] + best_match_size[1], top_left[1] + best_match_size[0])
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
    else:
        print("未识别到模板")

    # 显示结果
    cv2.imshow('Frame', frame)

    # 如果按下'q'键，则退出循环
    if recognized==best_match_filename or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()



print("[单圈模式]设置舵机角度为90.0°")
uservo.set_servo_angle(SERVO_ID, 60, interval=0) # 设置舵机角度 极速模式
uservo.wait() # 等待舵机静止
print("-> {}".format(uservo.query_servo_angle(SERVO_ID)))