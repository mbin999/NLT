# encoding=utf-8
import re
import pandas as pd
import os
cwd=os.getcwd()
'''
str = "分享视频 哈哈哈分享照片  北京·水碓子东路小区   懂-不的秒拍视频​​​"
str1 = "#王源#  王源源 @TFBOYS-王源   北京·五棵松文化体育中心  ​"
str2 = "lhgg说要带女朋友来#天安门#，既然你这么忙那我只能自己来啦[doge][doge][doge] 1321@22.com 北京·北京北大博雅国际酒店  ​​​"
str3 = "🤓[心]幸福的一天[心]🤓  北京  "
str4 = "愿赢球的喜悦能给每个人带来好运[太阳][太阳][可爱][可爱]  http://t.cn/R6tYbL7  ​​​12"
str5 = "@William威廉陈伟霆   三里屯的这家茶餐厅，狮子山下，味道还不错哦，有机会可以去吃吃 #陈伟霆#   北京·光大国际中心  ​​​"
str6 = "感谢 @飞乐鸟   @铁葫芦图书  和每位到场的朋友，这是我人生第一次新书分享会，感谢能有你们在。[害羞]  北京·飞乐鸟北京艺术中心（什刹海店）  ​​​"
str7 = "接下来一年，我希望在<SPAN style=COLOR: red>到更人性化，各东西。 地址：<A title=http://t.cn/8kUAX2z href=http://t.cn/8kU>"
str8 = "转发此条锦鲤，必有坏事发生 #日常迷信# #锦鲤#   北京·三里河 ​​​"
'''
#删<>里的内容
def dealkuohao(text):
    text = re.sub(r'<.*?>'," ",text)
    return text

#删##里的内容
def deal111(text):
    text = re.sub(r'#.*?#',' ',text)
    return text

#删@
def deal222(text):
    text = re.sub(r'@[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}',' ',text)
    return text

#删url
def dealUrl(text):
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    return text

#删表情
#\[(.{1,10})\]    这个匹配不同的表情
#\[([^ \[]*?)]   这个匹配每一个表情

def dealemo(text):
    text = re.sub(r'\[([^ \[]*?)]',' ',text)
    return text


#删邮箱
def dealem(text):
    text = re.sub(r'([a-zA-Z0-9%_.+\-]+)@([a-zA-Z0-9.\-]+?\.[a-zA-Z]{2,6})',' ',text)
    return text

#删转发(整条微博)
def dealtr(text):
    text = re.sub(r'转发.*?(好事|好运|中奖|运气|锦鲤|许愿|愿望|实现).*',' ',text)
    return text

#删分享，秒拍
def dealsh(text):
    text = re.sub(r'(分享|[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}秒拍|秒拍)(图片|照片|视频).*',' ',text)
    return text

#删【】
def deal333(text):
    text = re.sub(r'【.*?】',' ',text)
    return text

#删谁的微博视频
def dealoneself(text):
    text = re.sub(r'[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}的微博视频','',text)
    return text

#删复制这条信息(整条)
def dealcopy(text):
    text = re.sub(r'.*?复制这条信息，.*','',text)
    return text

def dealadd(text):
    text = re.sub(r'(北京|beijing|Beijing|BeiJing)·[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}','',text)
    return text

#删@ #等符号
def dealmore(text):
    text = re.sub(r'(@|#|\?\?\?|◆)','',text)
    return text

if __name__ == "__main__":
    '''   #print('hs----原:',str8)
    #text = dealtr(str8)
    #print('3333333:',text)
    text = dealsh(str)
    print('hs---1:',str)
    print('hs---2:',text)

'''
    #输入
    #hs = cwd + "/inputfile/" + "iclear.csv"
    data = pd.read_csv('inputfile/iclear.csv',encoding= 'utf-8')

    print('hs----origindata:',data.head())

    data['clean'] = 'hhh'   #建立一个字段，保存清洗后的文本.''中的内容是赋值，方便下步查找这个字段的列号

    print('hs----chouchou:',data.iat[1,11])#[1,11]中1为行号，11为列号，通过调整列号并打印，查找clean字段的所在列


    for i in range(len(data.content)):
        content1 = dealkuohao(data.content[i])
        content2 = deal111(content1)
        content3 = deal222(content2)
        content4 = dealUrl(content3)
        content5 = dealemo(content4)
        content6 = dealem(content5)
        content7 = dealtr(content6)
        content8 = dealsh(content7)
        content9 = deal333(content8)
        content = dealoneself(content9)
        content = dealcopy(content)
        content = dealadd(content)
        content = dealmore(content)
        data.iat[i,11] = content   #[i,11]i为了遍历所有行，11为clean字段所在的列，这一步不能选错

        print(i,content)

    data.to_csv('resultfile/oclear.csv',encoding='utf-8',index=False,sep=',')  #输出

