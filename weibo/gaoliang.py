#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import jieba
import jieba.analyse
from wordcloud import WordCloud
def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return [ backitems[i][1] for i in range(0,len(backitems))]
try:


    word_lst = []
    word_dict = {}
    with  open("cipin.txt") as wf2:  # 打开文件
        for word in wf2:
            nword = word.replace("\n", "")
            word_lst.append(nword.split(','))
            word_dict[nword.split(' ')[0].decode('utf-8')] = int( nword.split(' ')[1])

    sorted_word_dict = sort_by_value(word_dict)
    new_word_dict = {}
    i = 0
    maxword = 30
    for k in range(0, maxword):
        if (i < maxword):
            print "hlly--" +str(i), sorted_word_dict[k], word_dict[sorted_word_dict[k]]
            new_word_dict[sorted_word_dict[k]] = word_dict[sorted_word_dict[k]]
            i = i + 1



                    # 使用逗号进行切分
    """
    with open('fenci.txt') as wf, open("cipin.txt", 'w') as wf2:  # 打开文件
        for word in wf:
            nword = word.replace("\n", "")
            word_lst.append(nword.split(' '))  # 使用逗号进行切分
        for item in word_lst:
            for item2 in item:
                uitem2 = item2.decode('utf-8')
                if uitem2 not in word_dict:  # 统计数量
                    word_dict[uitem2] = 1
                else:
                    word_dict[uitem2] += 1

        sorted_word_dict = sort_by_value(word_dict)
        """


    cloud = WordCloud(

         #font_path="simkai.ttf",
         font_path="HYQiHei-25J.ttf",
         background_color='white',
         width=400,
         height=200,
         # 词云形状
         #mask=color_mask,
         # 允许最大词汇
         max_words=30,
         # 最大号字体
         max_font_size=40
     )
    #wordcloud = cloud.generate(mytext)
    wordcloud = cloud.generate_from_frequencies(new_word_dict)
    wordcloud.to_file("cloud1.jpg")  # 保存图片

    import matplotlib.pyplot as plt

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
except Exception ,e:
    print("--hlly--" +str(e))
    i=1

