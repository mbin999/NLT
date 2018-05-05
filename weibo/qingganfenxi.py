#encoding=utf-8
from snownlp import SnowNLP
# SnowNLP库：
# words：分词
# tags：关键词
# sentiments：情感度
# pinyin：拼音
# keywords(limit)：关键词
# summary：关键句子
# sentences：语序
# tf：tf值
# idf：idf值
s = SnowNLP(u'大哭]南锣鼓巷，烟袋斜街，什刹海，中央戏剧学院，鼓楼，恭王府 然后入手了个炫酷的墨镜→_→有种度假的feel，明天接我妈来北京购物[哈哈] 然后....我今天冲进exo代言的商品店激动的不知所措 嗯，大屏幕上是我男朋友都暻秀[微笑]   ​​​')
# s.words     # [u'这个', u'东西', u'真心', u'很', u'赞']
print(s.words)
s.tags # [(u'这个', u'r'), (u'东西', u'n'), (u'真心', u'd')
# , (u'很', u'd'), (u'赞', u'Vg')]
print(s.sentiments)
# s.sentiments  # 0.9769663402895832 positive的概率
# s.pinyin    # [u'zhe', u'ge', u'dong', u'xi', # u'zhen', u'xin', u'hen',
# u'zan']4
s = SnowNLP(u'「繁體字」「繁體中文」的叫法在臺灣亦很常見。')
# s.han      # u'「繁体字」「繁体中文」的叫法在台湾亦很常见。'
print(s.han)