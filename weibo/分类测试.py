#-------------------------------------
#版本： 1.0
#日期： 2018-05-18
#参考： http://blog.sciencenet.cn/blog-377709-1103593.html
#-------------------------------------

import pandas as pd
import jieba
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.cross_validation import cross_val_score
from sklearn import metrics

#读取原始数据
data = pd.read_csv('inputfile/train.csv',encoding='utf-8')
#待预测
predata = pd.read_csv('inputfile/prediction.csv',encoding='utf-8')

print('hs----读入数据：',data.head())

print('hs----数据的整体结构：',data.shape)


#定义方法（用结巴分词，并用空格隔开）
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

#定义方法（把停用词作为列表保存并返回）
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list

#划分特征x（文本内容）和标签y（心情分值）,需要根据自己的输入修改
x = data[['clearcontent']]
y = data.lei
x['cutted_content'] = x.clearcontent.apply(chinese_word_cut)
#待预测数据
print(predata.head())
prex = predata[['clean']]
prex['cut'] = prex.clean.apply(chinese_word_cut)

#划分训练样本和测试样本。random_state取1保证不同环境，随机数取值一致
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

print('hs----xtrain',x_train.shape) #训练集与实验集3:1（默认）
print('hs-----xtrainhead:',x_train.head())
print('hs----xtest',x_test.shape) #训练集与实验集3:1（默认）
print('hs----ytrain',y_train.shape) #训练集与实验集3:1（默认）
print('hs----ytest',y_test.shape) #训练集与实验集3:1（默认）

# 获取停用词表文件，并列表化
stop_words_file = "dict/hgdstopwords.txt"
stopwords = get_custom_stopwords(stop_words_file)

#print('hs-----停用词列最后十个 ：',stopwords[-10:])

#不加停用词，对x（分词）训练集进行向量化
#vect = CountVectorizer()
#term_matrix = pd.DataFrame(vect.fit_transform(x_train.cutted_content).toarray(),columns=vect.get_feature_names())
#print('hs----分词后向量化(不加停用词) ：',term_matrix.head())
#print('hs----分词后向量化形状（不加停用词） ：',term_matrix.shape)

#只加停用词表，对x（分词）训练集进行向量化
#vect1 = CountVectorizer(stop_words=frozenset(stopwords))
#term_matrix1 = pd.DataFrame(vect1.fit_transform(x_train.cutted_content).toarray(),columns=vect1.get_feature_names())
#print('hs----分词后向量化(加停用词表) ：',term_matrix1.head())
#print('hs----分词后向量化形状（加停用词表） ：',term_matrix1.shape)

#加更多过滤，对x（分词）训练集进行向量化
max_df = 0.8     #超过比例，删
min_df = 3       #低于数量，删
vect2 = CountVectorizer(max_df = max_df,
                        min_df = min_df,
                        token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b',
                        stop_words=frozenset(stopwords))
term_matrix2 = pd.DataFrame(vect2.fit_transform(x_train.cutted_content).toarray(),columns=vect2.get_feature_names())

print('hs----分词后向量化（更多去除）(数据框) ：',term_matrix2.head())
#print('hs----分词后向量化形状（更多去除） ：',term_matrix2.shape)

#采用朴素贝叶斯分类模型
nb = MultinomialNB()

#建立管道，串联vect和nb
pipe = make_pipeline(vect2, nb)

#print('hs----pipe步骤：',pipe.steps)

#添加y（心情值）训练数据，做交叉检验，算出模型分类准确率的均值
cross_val_score(pipe, x_train.cutted_content, y_train, cv=5, scoring='accuracy').mean()
print('hs--检测 ：',cross_val_score(pipe, x_train.cutted_content, y_train, cv=5, scoring='accuracy').mean())

#用训练集拟合模型
pipe.fit(x_train.cutted_content, y_train)
#print('hs---what:',hs)


y_pre = pipe.predict(x_test.cutted_content)

#预测分类准确率的平均值
ceshi = metrics.accuracy_score(y_test,y_pre)
print('hs---预测结果：',ceshi)

#预测混淆矩阵
hxjz = metrics.confusion_matrix(y_test,y_pre)
print('hs---预测混淆矩阵：',hxjz)

#对待预测数据进行预测
hhpre = pipe.predict(prex.cut)
predata['s'] = hhpre
print('hhhhh:   ',hhpre)
predata.to_csv("resultfile/biaozhu",index=False,sep=',')
