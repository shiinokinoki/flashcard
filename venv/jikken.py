import cv2
import numpy as np
# ocr_card.py
import os
from PIL import Image
import pyocr
import pyocr.builders


"""
Ⅰ.ノイズ除去＆2値化
Ⅱ.OCRの実行(テキストデータ化)
Ⅲ."OCRがどこを読み取ったのかを可視化
"""



"""Ⅰ.ノイズ除去＆2値化"""

path='machine_learning\img_folda\yousyo3.png'
img = cv2.imread(path)

ksize = 20
blur = cv2.blur(img, (ksize, ksize))
rij = img/blur
index_1 = np.where(rij >= 1.00) # 1以上の値があると邪魔なため
rij[index_1] = 1
rij_int = np.array(rij*255, np.uint8) # 除算結果が実数値になるため整数に変換
rij_HSV = cv2.cvtColor(rij_int, cv2.COLOR_BGR2HSV)
ret, thresh = cv2.threshold(rij_HSV[:,:,2], 0, 255, cv2.THRESH_OTSU)
rij_HSV[:,:,2] = thresh
rij_ret = cv2.cvtColor(rij_HSV, cv2.COLOR_HSV2BGR)

cv2.imwrite("result3.png", rij_ret)
cv2.imshow('image', rij_ret)
cv2.waitKey(0)
cv2.destroyAllWindows()




"""Ⅱ.OCRの実行(テキストデータ化)"""

# 1.インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# 2.OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 3.原稿画像の読み込み
img_org = Image.open("result3.png")

# 4.ＯＣＲ実行
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
result = tool.image_to_string(img_org, lang="eng", builder=builder)

print(result)




"""Ⅲ.OCRがどこを読み取ったのかを可視化"""

builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
res = tool.image_to_string(Image.open("result3.png"),lang="eng",builder=builder)
out = cv2.imread("result3.png")
for d in res:
    print(d.content) #どの文字として認識したか
    print(d.position) #どの位置を検出したか
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) #検出した箇所を赤枠で囲む
 
#検出結果の画像を保存
cv2.imwrite("result3_where.png", out)
#検出結果の画像を表示
cv2.imshow("img",out)
cv2.waitKey(0)
cv2.destroyAllWindows()
