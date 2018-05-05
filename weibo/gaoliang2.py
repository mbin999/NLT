#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import jieba
import jieba.analyse
"""
wf = open('fenci.txt', 'w+')

# 创建停用词list
def stopwordslist(filepath):
    stopwords = []
    with open(filepath) as wf:

        for word in wf:
            nword1 = word.replace("\n", "")
            nword = word.strip('\n\r').split('\t')
            stopwords = stopwords+ (nword1.split(','))  # 使用逗号进行切分



    #stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

for line in open('baiyun.csv'):
    item = line.strip('\n\r').split('\t') # 制表格切分
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径

    tags = jieba.analyse.extract_tags(item[0]) # jieba分词
    outstr = ''
    for word in tags:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    tagsw = ",".join(tags) # 逗号连接切分的词
    if not (tagsw==''):
        wf.write(outstr+'\n')

wf.close()
"""
try:
    filename = "fenci.txt"
    comment_text = open(filename, 'r').read()
    with open(filename) as f:
     mytext = f.read()
     from wordcloud import WordCloud

     mytext = " ".join(jieba.cut(comment_text))
     cloud = WordCloud(

         #font_path="simkai.ttf",
         font_path="HYQiHei-25J.ttf",

         background_color='white',
         # 词云形状
         #mask=color_mask,
         # 允许最大词汇
         max_words=2000,
         # 最大号字体
         max_font_size=40
     )
     wordcloud = cloud.generate(mytext)

     wordcloud.to_file("cloud1.jpg")  # 保存图片

     import matplotlib.pyplot as plt

     plt.imshow(wordcloud, interpolation='bilinear')
     plt.axis("off")
     plt.show()
except Exception ,e:
    print("--hlly--" +str(e))
    i=1

