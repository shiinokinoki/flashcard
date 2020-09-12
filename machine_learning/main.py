

from module import OCR
import os

# インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += path_tesseract


print(OCR('machine_learning\img_folda\yousyo1.jpg'))