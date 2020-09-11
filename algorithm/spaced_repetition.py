import math

#SM2の実装
#https://www.supermemo.com/en/archives1990-2015/english/ol/sm2

#intervalとe_factor を計算する。これらは漸化式的に決まるので前のintervalとe_factorが必要
#interval: 次の復習までの時間(日)　最初は1日、次は6日、それ以降はinterval * e_factor
    #間違えると(すなわちquality of response < 3) e_factor は更新されずにinterval = 1
#e_factor: easiness factor アイテムの簡単さを表す。初期値は2.5に設定せよ　1.3以上　2.5以下？　1.3が最も難しい 表す 1.3以上の値で1.3が最も難しい　2.5以下ということが書いてあったが,載ってたアルゴリズムには2.5以下におさえるような仕組みは見当たらなかった
#quality of response: アイテムへの回答の質　0から5の整数値が想定されていたが連続値でも問題なさそう　簡易的に正解だったら5,不正解なら0でもいいかも？　それか回答に要する時間で評価？
    # 5 - perfect response
    # 4 - correct response after a hesitation
    # 3 - correct response recalled with serious difficulty
    # 2 - incorrect response; where the correct one seemed easy to recall
    # 1 - incorrect response; the correct one remembered
    # 0 - complete blackout.
def calculate_interval_and_e_factor(interval, e_factor, quality_of_response):
    if quality_of_response < 3:
        return 1, e_factor
    else:
        #e_factorを更新
        e_factor += 0.1 - (5 - quality_of_response) * (0.03 + (5 - quality_of_response) * 0.02)
        if e_factor < 1.3:
            e_factor = 1.3
        #interval
        if interval ==0:
            interval = 1
        elif interval == 1:
            interval = 6
        else:
            interval = math.ceil(interval * e_factor)
        
        return interval, e_factor

#クラスにしてみた
class Item:
    def __init__(self):
        self.e_factor = 2.5 
        self.interval = 0 
    
    
    def update_interval_and_e_factor(self, quality_of_response):
        self.interval, self.e_factor = calculate_interval_and_e_factor(self.interval, self.e_factor, quality_of_response)


item = Item()
q_responses = [0,1,1,3,4,5,5,5,5,1,2,5,5,5]
for q in q_responses:
    print(item.interval)
    item.update_interval_and_e_factor(q)

#正解してるとインターバルはすぐおおきくなるが、間違えるとまたでてくるようになる