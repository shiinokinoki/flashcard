# インポート
import os
from PIL import Image
import pyocr
from pyocr import builders
import cv2


class OCR():
    def __init__(self, img_path):
        self._save_where_path = 'result_where.png'

        # preprocessingで得たがそう(save_file)
        self.save_imgfile = img_path
        self._tesseract()
        self.tool = self._ocr_engine()

    @staticmethod
    def _tesseract():
        """インストール済みのTesseractのパスを通す"""
        path_tesseract = "C:\\Program Files\\Tesseract-OCR"
        if path_tesseract not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep + path_tesseract

    @staticmethod
    def _ocr_engine():
        """OCRエンジンの取得"""
        tools = pyocr.get_available_tools()
        return tools[0]

    def text_get(self):
        """ＯＣＲ実行(テキストデータ化)"""
        # builderにTextBuilderを指定
        builder = builders.TextBuilder(tesseract_layout=6)
        # テキストデータを取得
        result = self.tool.image_to_string(Image.open(
            self.save_imgfile), lang="eng", builder=builder)
        return result

    def where_get(self,save_where_path=""):
        """ＯＣＲがどこを読み取ったか可視化"""
        if save_where_path != "":
            self._save_where_path = save_where_path
        
        # builderにWordBoxBuilderを指定
        builder = builders.WordBoxBuilder(tesseract_layout=6)
        res = self.tool.image_to_string(Image.open(
            self.save_imgfile), lang="eng", builder=builder)
        out = cv2.imread(self.save_imgfile)
        for d in res:
            # どの文字として認識したか
            print(d.content)
            # どの位置を検出したか
            print(d.position)
            # 検出した箇所を赤枠で囲む
            cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)
        # 検出結果の画像を保存
        cv2.imwrite(self._save_where_path, out)
