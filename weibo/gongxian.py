# -*- coding: utf-8 -*-
import os
import xlrd
import re
from pprint import pprint as pt
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')


def readxls(path):
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]
    data = []
    for i in range(0, sheet.ncols):
        data.append(list(sheet.col_values(i)))
    return (data[0])

def readtxt(path):
    word_lst = []
    with codecs.open(path, 'r')as f:
        for word in f:
            nword = word.replace("\n", "")
            word_lst.append(nword)  # 使用逗号进行切分
    return word_lst




def wryer(path, text):
    with open(path, 'w') as f:
        f.write(text)
    return path+' is ok!'


def buildmatrix(x, y):
    return [[0 for j in range(y)] for i in range(x)]

"""
def dic(xlspath):
    keygroup = readxls(xlspath)
    keytxt = ','.join(keygroup)
    keyfir = keytxt.split(',')
    #keylist = list(set((key for key in keytxt.split(',') if key != '']))
    keylist = list(set([key for key in keytxt.split(',') if key != '']))
    keydic = {}
    pos = 0
    for i in keylist:
        pos = pos+1
        keydic[pos] = str(i)
    return keydic
"""
def dic(cipinpat,cipinbiggerthan,cipinacount):
    word_lst = []
    word_dict = {}
    count = 0
    firstline = True

    import codecs


    with codecs.open(cipinpat, 'r','utf-8-sig')as f:
        for word in f:
            nword = word.replace("\n", "")
            if int(nword.split(' ')[1]) >cipinbiggerthan:
                word_lst.append(nword.split(' ')[0])
                count = count +1
            if count >=cipinacount:
                break

    pos = 0
    for i in word_lst:
        pos = pos+1
        word_dict[pos] = str(i)
    return word_dict



def listvalue(xlspath):
    keygroup = readtxt(xlspath)
    keytxt = ','.join(keygroup)
    keyfir = keytxt.split(',')
    #keylist = list(set((key for key in keytxt.split(',') if key != '']))
    keylist = list(set([key for key in keytxt.split(',') if key != '']))

    return keylist


def showmatrix(matrix):
    matrixtxt = ''
    count = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            matrixtxt = matrixtxt+str(matrix[i][j])+'\t'
        matrixtxt = matrixtxt[:-1]+'\n'
        count = count+1
        print('No.'+str(count)+' had been done!')
    return matrixtxt


def inimatrix(matrix, dic, length):
    matrix[0][0] = '+'
    for i in range(1, length):
        matrix[0][i] = dic[i]
    for i in range(1, length):
        matrix[i][0] = dic[i]
    # pt(matrix)
    return matrix


def countmatirx(matrix, dic, mlength, keylis):
    for i in range(1, mlength):
        for j in range(1, mlength):
            count = 0
            for k in keylis:
                ech = str(k).split(',')
                # print(ech)
                if str(matrix[0][i]) in ech and str(matrix[j][0]) in ech and str(matrix[0][i]) != str(matrix[j][0]):
                    count = count+1
                else:

                    continue
            matrix[i][j] = str(count)
    return matrix

def count_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    keywordlist=matrix[0][1:]  #列出所有关键词
    appeardict={}  #每个关键词与 [出现在的行(formated_data)的list] 组成的dictionary
    for w in keywordlist:
        appearlist=[]
        i=0
        for each_line in formated_data:
            if w in each_line:
                appearlist.append(i)
            i +=1
        appeardict[w]=appearlist
    print "----共----" + str(len(matrix)-1) + "---行"
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        print "----第----" + str(row) + "---行"
        for col in range(1, len(matrix)):
                # 遍历矩阵第一列，跳过下标为0的元素
                # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if col >= row:
                #仅计算上半个矩阵
                if matrix[0][row] == matrix[col][0]:
                    # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                    matrix[col][row] = str(0)
                else:
                    counter = len(set(appeardict[matrix[0][row]])&set(appeardict[matrix[col][0]]))

                    matrix[col][row] = str(counter)
            else:
                matrix[col][row]=matrix[row][col]
    return matrix

def format_data(data,set_key_list):

    formated_data = []
    for ech in data:
        ech_line = ech.split(',')

        temp=[]
        for e in ech_line:
            if e in set_key_list:
                temp.append(e)
        ech_line=temp

        ech_line = list(set(filter(lambda x: x != '', ech_line)))
        formated_data.append(ech_line)
    return formated_data
def main():
    fencipath = r'fenci.txt'#分词后生成的文件
    cipinpath = r'cipin.txt'
    wrypath = r'result.txt'
    cipinbiggerthan = 10
    cipinacount = 100

    keylis = readtxt(fencipath)
    keydic = dic(cipinpath,cipinbiggerthan,cipinacount)
    keylist = listvalue(fencipath)
    formatdata = format_data(keylis,keylist)
    length = len(keydic)+1
    matrix = buildmatrix(length, length)
    print('Matrix had been built successfully!')
    matrix = inimatrix(matrix, keydic, length)
    print('Col and row had been writen!')
    #matrix = countmatirx(matrix, keydic, length, keylis)
    matrix1 = count_matrix(matrix,formatdata)
    print('Matrix had been counted successfully!')
    matrixtxt = showmatrix(matrix1)
    #pt(matrix)
    print(wryer(wrypath, matrixtxt))
    #print(keylis)




if __name__ == '__main__':
    main()