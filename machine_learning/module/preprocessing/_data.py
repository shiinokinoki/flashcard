# なるべくアノテーションはつけてもらえるとみやすいです．

class Image_for_ocr():
    def __init__(self,path:str):
        '''
        path: 画像のパス
        self._img :出力画像
        self._size: 画像サイズ
        self._preimg :元の画像
        '''
        pass
        
    def fit(self):
        '''
        self._binarization()
        self._noise_remove()
        self._canny()
        ...
        return self._img
        みたいな...？
        '''
        pass

    @property
    def img(self):
        return self_img

    @property
    def size(self):
        return self._size

    def _noise_remove(self):
        '''ノイズを除去する'''
        pass

    def _binarization(self):
        '''白黒にする'''
        pass

    def _canny():
        '''canny法とか？'''
        pass

    def hogehoge(self):
        pass


