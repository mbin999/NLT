# encoding=utf-8
# ------------------------------------------
#   版本：1.0
#   日期：2018-05-4
#   作者：gracewu
#   参考：
# ------------------------------------------
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
cwd=os.getcwd() #
#原始文件
originalfile = cwd + "/inputfile/" + "buu0503fenci2.txt"
#停用词
stopfile = cwd + "/dict/" + "stopwords.txt"
#结果
cipinresult = cwd + "/resultfile/" + "buucipin.txt"
#分词分割符号
fenciseparator = "/"
#分割符号
cipinseparator = " "
#分词的结果进行排序
def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return [ backitems[i][1] for i in range(0,len(backitems))]
word_lst = []
word_dict = {}
with open(originalfile) as wf, open(cipinresult, 'w') as wf2: #    打开文件
    #逐行读入每个词到word_lst
    for word in wf:
        nword = word.replace("\n", "")
        word_lst.append(nword.split(fenciseparator))  # 使用separator进行切分
    #遍历每个词，出现的次数写入word_dict,例如word_dict["什刹海"]=7
    for item in word_lst:
        for item2 in item:
            if item2 not in word_dict: #                 统计数量
                word_dict[item2] = 1
            else:
                word_dict[item2] += 1
    #按词频大小排序
    sorted_word_dict = sort_by_value(word_dict)
    #word_dict_list = word_dict.items().sort()

    for key in sorted_word_dict:
        print key, word_dict[key]
        wf2.write(key + cipinseparator + str(word_dict[key]) + '\n') #  写入文档
