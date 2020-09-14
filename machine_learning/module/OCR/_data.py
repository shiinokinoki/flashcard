# インポート
import os
from PIL import Image
import pyocr
import pyocr.builders

class ocr():
    def __init__(self):

        self.save_where_path = 'result_where.png'
        #preprocessingで得たがそう(save_file)
        self.save_file = 'result.png'
        

    def tesseract(self):
        """インストール済みのTesseractのパスを通す"""
        path_tesseract = "C:\\Program Files\\Tesseract-OCR"
        if path_tesseract not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep + path_tesseract
        

    def ocr_engine(self):
        """OCRエンジンの取得"""
        tools = pyocr.get_available_tools()
        tool = tools[0]
        return tool
    
    def text_get(self):
        """ＯＣＲ実行(テキストデータ化)"""
        # builderにTextBuilderを指定
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        # テキストデータを取得
        result = tool.image_to_string(Image.open(self.save_file), lang="eng", builder=builder)
        return result

    def where_get(self):
        """ＯＣＲがどこを読み取ったか可視化"""
        # builderにWordBoxBuilderを指定
        builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
        res = tool.image_to_string(Image.open(self.save_file),lang="eng",builder=builder)
        out = cv2.imread(self.save_file)
        for d in res:
            # どの文字として認識したか
            print(d.content) 
            # どの位置を検出したか
            print(d.position) 
            #検出した箇所を赤枠で囲む
            cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) 
        #検出結果の画像を保存
        cv2.imwrite(self.save_where_path, out)


