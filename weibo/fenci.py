# encoding=utf-8
# ------------------------------------------
#   版本：1.0
#   日期：2018-05-4
#   作者：gracewu
#   参考：https://blog.csdn.net/kevinelstri/article/tails/70054355
# ------------------------------------------
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import jieba
import os
cwd=os.getcwd() #

#原始文件
originalfile = cwd +  "/inputfile/" + "bjlhdx.csv"
#停用词
stopfile = cwd + "/dict/" + "stopwords.txt"
#自定义词库
userdict =  cwd + "/dict/" + "userdict.txt"
#分词结果
fenciresult = cwd + "/resultfile/" + "buu0503fenci.txt"
#停用词分割符号
stopwordsseparator = ","

# 读取停用词写入list
def stopwordslist(filepath):
    stopwords = []
    with open(filepath) as wf:
        for word in wf:
            nword1 = word.replace("\n\r", "").replace("\n","")
            stopwords = stopwords+ (nword1.split(stopwordsseparator))  # 使用逗号进行切分
    return stopwords

try:
    wf1 = open(fenciresult, 'w+')
    inputs = open(originalfile, 'r')
    stopwords = stopwordslist(stopfile)  # 这里加载停用到stopwords
    jieba.load_userdict(userdict)  # 这里加载自定义词库
    for line in inputs:
        item = line.strip('\n\r').strip('\n').strip().split('\t') # 制表格切分
        tags1 = list(jieba.cut(item[0].strip()))
        outstr = ''
        for word in tags1:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += "/"

        if  (tags1 ):
            wf1.write(outstr+'\n')

        #tasw1 = "/".join(tags1)
        print("-hlly-original-" + item[0])
        print("-hlly-cut-" + outstr)

except Exception, e:
    print ("----hlly----" + str(e))
    i =1
wf1.close()
