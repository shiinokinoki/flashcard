# インポート
import cv2
import numpy as np


class Image_for_ocr():
    def __init__(self,path:str):
        # ksize(ハイパーパラメーター)の設定
        ksize = 50
        self.ksize = ksize
        self.save_file = 'result.png'
        

    def _noise_remove(self):
        '''ノイズを除去する'''
        # ぼかす(平滑化)
        self.blur = cv2.blur(_img, (self.ksize, self.ksize))
        

    def _binarization(self):
        '''画像の影を除去（大津の方法 2値化）'''
        
        # 凹凸係数の算出
        rij = self.img / self.blur
        # rijが1以上のところは全て1に統一する(邪魔なので)
        index_1 = np.where(rij >= 1.00)
        rij[index_1] = 1
        # 除算結果が実数値になるため整数に変換
        rij_int = np.array(rij*255, np.uint8) 
        # BGRからHSVに変換
        rij_HSV = cv2.cvtColor(rij_int, cv2.COLOR_BGR2HSV)
        # 自動閾値設定(自分で設定する必要なし)
        ret, thresh = cv2.threshold(rij_HSV[:,:,2], 0, 255, cv2.THRESH_OTSU) 
        # V(明度)を閾値にする
        rij_HSV[:,:,2] = thresh
        # HSVからBGRに変換
        rij_ret = cv2.cvtColor(rij_HSV, cv2.COLOR_HSV2BGR)
        return rij_ret

    def get_img(self,path):
        """画像を保存"""
        self.img = cv2.imread(path)
        cv2.imwrite(self.save_file, rij_ret)
        

