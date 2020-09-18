import json
import sqlite3
from googletrans import Translator
import nltk
from nltk.corpus import stopwords
import re

class After_ocr():
    def __init__(self,json_name):
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')
        nltk.download('punkt')

        self._file_name = json_name # 保存ファイル名
        self.__using_type = ['JJ','JJR','JJS','NN','NNS','NNP','NNPS',
                         'RB','RBR','RBS','VB','VBD','VBG','VBN','VBP',
                            'VBZ']
        symbol = {"'", '"', ':', ';', '.', ',', '-', '!', '?', "'s",'/'}
        self.__stopset = set(stopwords.words('english')) | symbol

    def run(self, text:str):
        '''
        ocrによって吐き出された単語に対して実行する
        '''
        words = nltk.word_tokenize(text)
        words = self._remove_stopwords(words)
        self._selected = []
        for word, part_of_speech in nltk.pos_tag(words):
            if part_of_speech in self.__using_type:
                self._selected.append(word)
        self._words_to_json()
    
    def _remove_stopwords(self, words:list)->list:
        '''
        stopsetに入っているものを除外する
        '''
        return [s for s in words if self._choose(s)]

    def _choose(self, s) -> bool:
        if s.lower() in self.__stopset:
            return False
        if len(s) < 3:
            return False
        if re.match(r'[^\W\d]*$', s)==False:
            return False
        return True


    def _words_to_json(self):
        '''
        文字を翻訳しjson形式で保存する
        '''
        
        meaning_dict_list = []

        for word in self._selected:
            meaning_dict_list.append(self._translate(word))

        with open(self._file_name, mode="w",encoding='utf-8') as f:
            d = json.dumps(meaning_dict_list,indent=2, ensure_ascii=False)
            f.write(d)

    def _translate(self, word: str) -> dict:
        '''
        wordを翻訳する．基本的には辞書を使って行うが，辞書になかった場合はgoogleの翻訳に頼る．
        '''
        word = '"'+word+'"'
        conn = sqlite3.connect("./wordbook/pymodule/machine_learning/module/NL_processing/ejdict.sqlite3")
        raw_meanings = list(conn.execute('select mean from items where word='+word))
        ans_meanings = []
        word = word.replace('"', '')
        
        if len(raw_meanings) != 0:
            #辞書が使える時
            for x in raw_meanings:
                ans_meanings.extend((x[0].split('/')))
        else:
            #辞書が使えないのでgoogletransを使う．
            translator = Translator()
            tmp_text = translator.translate(word, dest='ja').text
            if not tmp_text.isalpha():
                ans_meanings.append(tmp_text) 
        ans_dict = {'name':word,'meaning':ans_meanings}
        conn.close()
        return ans_dict
    
    @property
    def select_words(self):
        return self._selected