import cv2
import pytesseract
# 读取图像
img = cv2.imread('example.png')
# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 进行二值化处理
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# 使用 Tesseract 进行字符识别
text = pytesseract.image_to_string(thresh, lang='eng')
# 输出识别结果
print(text)

