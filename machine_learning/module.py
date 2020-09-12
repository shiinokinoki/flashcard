## OCRモジュール

#インポート
from PIL import Image, ImageTk
import pyocr
import pyocr.builders

from preprocessing import *
from NL_processing import *

def image_for_ocr():
    '''preprocessingを使う'''
    pass


def OCR(img_path):
    '''この下は前処理だから適宜書き直す
    # OCRエンジンの取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 原稿画像の読み込み
    img_org = Image.open(img_path)
    img_rgb = img_org.convert("RGB")
    pixels = img_rgb.load()

    # 原稿画像加工（黒っぽい色以外は白=255,255,255にする）
    c_max = 169
    for j in range(img_rgb.size[1]):
        for i in range(img_rgb.size[0]):
            if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
                    pixels[i, j][0] > c_max):
                pixels[i, j] = (255, 255, 255)
    '''

    # ＯＣＲ実行
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img_rgb, lang="eng", builder=builder)

    return result

    def after_ocr():
        '''NLprocessingを使って書く'''
        pass


