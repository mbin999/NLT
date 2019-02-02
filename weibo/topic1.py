# encoding=utf-8
# ------------------------------------------
#   版本：1.0
#   日期：2018-05-4
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
originalfile = cwd + "/inputfile/" + "icixingandfenci.csv"
#原始文件编码
originalfil_encoding = "utf-8"
#结果
topicresult = cwd + "/resultfile/" + "otopic.xlsx"
#topicresult1 = cwd + "/resultfile/" + "121.xlsx"
#特征关键词个数
n_features = 20
#每个主题输出前n个关键词。
n_top_words = 10
#主题数
n_topics = 2

#打印每个主题下权重较高的词
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
            for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()



def chinese_word_cut(mytext):
    #return " ".join(jieba.cut(mytext))  #结巴分词
    return " ".join(jieba.analyse.extract_tags(mytext))  #结巴分词基于 TF-IDF 算法的关键词
    #return " ".join(jieba.analyse.textrank(mytext))  #结巴分词基于TextRank算法的关键词
try:
    df = pd.read_csv(originalfile,encoding=originalfil_encoding)

    print('1111:',df.head())

    print('2222:',df.shape)

    df["content_cutted"] = df.content.apply(chinese_word_cut)
    print('3333:',df.content_cutted.head())

    #保存分词结果
    #df.to_excel(topicresult)

    #词汇统计向量
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english')

    tf = tf_vectorizer.fit_transform(df.content_cutted)

    #LDA主题模型训练
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)


    tf_feature_names = tf_vectorizer.get_feature_names()

    print_top_words(lda, tf_feature_names, n_top_words)



    #打印每行所属主题
    tdp = lda.transform(tf)
    print("hhhhh:",tdp.shape)
    tdp1 = DataFrame(tdp)
    tdp1.to_excel(topicresult)






except Exception ,e:
    print("--hlly--" +str(e))
    i=1

