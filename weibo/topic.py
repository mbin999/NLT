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
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import os
cwd=os.getcwd() #

#原始文件
originalfile = cwd + "/inputfile/" + "bjlhdx2.csv"
#原始文件编码
originalfil_encoding = "utf-8"
#结果
topicresult = cwd + "/resultfile/" + "buutopic2.xlsx"
#特征关键词个数
n_features = 100
#每个主题输出前n个关键词。
n_top_words = 20

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
    #df = pd.read_csv("test3.csv", encoding='gb18030')
    print(df.head())
    df.shape
    print(df.shape)

    df["content_cutted"] = df.content.apply(chinese_word_cut)
    print df.content_cutted.head()
    print df.content_cutted

    df.to_excel(topicresult)
    n_features = 100
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=10)


    tf = tf_vectorizer.fit_transform(df.content_cutted)

    n_topics = 5
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)

    n_top_words = 20
    tf_feature_names = tf_vectorizer.get_feature_names()

    print_top_words(lda, tf_feature_names, n_top_words)


    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)



    pyLDAvis.enable_notebook()
    pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)



except Exception ,e:
    print("--hlly--" +str(e))
    i=1

