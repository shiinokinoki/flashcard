from module.preprocessing import Image_for_ocr
from module.OCR import OCR
from module.NL_processing import After_ocr


class All_process():
    def __init__(self, show_where=False):
        self.__img_path = 'result.png'
        self.__json_name = 'save.json'
        self._show_where = show_where

        self.pre = Image_for_ocr(self.__img_path)
        self.ocr = OCR(self.__img_path)
        self.after = After_ocr(self.__json_name)

    def run(self, img_path='sample.png', where_path='where.png'):
        self.pre.get_img(img_path)
        text = self.ocr.text_get()
        if self._show_where:
            self.ocr.where_get(where_path)
        self.after.run(text)


def img_to_json(img_path='./img_folder/yousyo0.png', show_where=False):
    ap = All_process(show_where)
    ap.run(img_path)


if __name__ == '__main__':
    img_to_json(show_where=True)
