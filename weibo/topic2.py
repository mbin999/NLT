# encoding=utf-8
# ------------------------------------------
#   版本：2.0
#   日期：2019-03-4
#   作者：gracewu
#   参考：https://blog.csdn.net/TiffanyRabbit/article/details/76445909
#   参考：https://www.jianshu.com/p/fdde9fc03f94
# ------------------------------------------
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import jieba
import jieba.analyse
import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import os
cwd=os.getcwd() #

#原始文件
originalfile = cwd + "/inputfile/" + "0118fenci.csv"
#原始文件编码
originalfil_encoding = "utf-8"
#停用词
stopfile = cwd + "/dict/" + "stopwords.txt"
#自定义词库
userdict =  cwd + "/dict/" + "userdict.txt"
#停用词分割符号
stopwordsseparator = ","
#结果
topicresult = cwd + "/resultfile/" + "0118topic.xls"
topicresult1 = cwd + "/resultfile/" + "0118topic0304-1.xls"
#特征关键词个数
n_features = 100
#每个主题输出前n个关键词。
n_top_words = 10
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
            for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

# 读取停用词写入list
def stopwordslist(filepath):
    stopwords = []
    with open(filepath) as wf:
        for word in wf:
            nword1 = word.replace("\n\r", "").replace("\n","")
            stopwords = stopwords+ (nword1.split(stopwordsseparator))  # 使用逗号进行切分
    return stopwords
def chinese_word_cut(mytext):
    #return " ".join(jieba.cut(mytext))  #结巴分词
    item = mytext.strip('\n\r').strip('\n').strip().split('\t')  # 制表格切分
    tags1 = list(jieba.cut(item[0].strip()))
    outstr = ''
    for word in tags1:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "

    return outstr.rstrip(" ")
    #return " ".join(jieba.analyse.extract_tags(mytext))  #结巴分词基于 TF-IDF 算法的关键词
    #return " ".join(jieba.analyse.textrank(mytext))  #结巴分词基于TextRank算法的关键词
try:
    df = pd.read_csv(originalfile,encoding=originalfil_encoding)
    #df = pd.read_csv("test3.csv", encoding='gb18030')
    print(df.head())
    df.shape
    print(df.shape)

    stopwords = stopwordslist(stopfile)  # 这里加载停用到stopwords
    jieba.load_userdict(userdict)  # 这里加载自定义词库

    df["content_cutted"] = df.content.apply(chinese_word_cut)
    print df.content_cutted.head()
    print df.content_cutted

    df.to_excel(topicresult)
    n_features = 100
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.8,
                                    min_df=5)


    tf = tf_vectorizer.fit_transform(df.content_cutted)

    n_topics = 4
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)

    n_top_words = 30
    tf_feature_names = tf_vectorizer.get_feature_names()

    print_top_words(lda, tf_feature_names, n_top_words)
    #打印每行所属主题
    tdp = lda.transform(tf)
    print("hhhhh:",tdp.shape)

    from xlrd import open_workbook
    from xlutils.copy import copy

    rexcel = open_workbook(topicresult)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    values = ["1", "2", "3"]
    #row = rows
    for row in range(0,len(tdp)):
        i = row
        for k in range(0,n_topics):
            table.write(row+1, 4+k, tdp[i][k])  # xlwt对象的写方法，参数分别是行、列、值

    excel.save(topicresult1)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel

    #tdp1 = DataFrame(tdp)
    #tdp1.to_excel(topicresult)


    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)



    pyLDAvis.enable_notebook()
    pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)



except Exception ,e:
    print("--hlly--" +str(e))
    i=1

