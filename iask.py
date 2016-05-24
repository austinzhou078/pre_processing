# -*- coding:utf-8 -*-
__author__ = 'Austin'

import re
import os
import os.path
import time

rootdir = "/Users/Austin/360云盘/论文/test/iask"

#分数计算函数
# 3年级，还不能用方程吧？算术解法如下： 爸爸比小刚大36-8=28岁爸爸年龄是小刚年龄3倍的时候，年龄差还是28岁所以那时候28就是小刚年龄的2倍那时小刚的年龄为：28/2-14岁14-8=6所以再过6年，爸爸的年龄是小刚的3倍)$||1096233934
# 设再过a年3*(8+a)=36+a求得a=6)$||1554541737
# 解:设小刚现在x岁     3x=(x-8）+36     3x=x-8+36   3x-x=36-8     2x=28       x=14     14-8=6)$||1400316954}

def norma(text):
    text2 = re.sub('(\!|\！|`|\~|\～|\。|\,|\.|\-|\?|\？|\·){2,}',' ',text)
    return text2

def score_comput(ans):
    l = len(ans)
    score = 1/(abs(l-100.1))

    return score

#     return 1/len(ans)
def modify(ans):
    return re.search('.*(?=\)\$\|\|)', ans).group()

# 高端玩法，全自动化
# for parent,dirnames,filenames in os.walk(rootdir):
#     # for dirname in  dirnames:                       #输出文件夹信息
#     #     print "parent is: " + parent
#     #     print  "dirname is: " + dirname
#     for filename in filenames:                        #输出文件信息
#         print "parent is: " + parent
#         print "filename is: " + filename
#         print "the full name of the file is: " + os.path.join(parent,filename) #输出文件路径信息
#         print "\n"
#
#     print "------------------------\n"

i = 0

for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:         # 遍历每一个文件
        # print parent                   # /Users/Austin/360云盘/论文/test/yahoo
        print filename                 # mOut (9)
        file = str(os.path.join(parent,filename)) #输出文件路径信息
        l = open(str(file), 'r')

        #当前目录下新建一个文件来存放筛选出来的数据,用数字1-n表示
        new_dir = parent
        new_dir += "/result/"
        new_dir += str(i)
        i += 1
        new_dir += ".txt"
        f = open(new_dir, 'w')


        for text in l:  #同一个file中的每一句话


            # print text
            title = re.search('.*(?=\$\{\*)', text)

            answer = re.search('(?<=\$\{\*\$\().*(?=\$2)', text)

            if answer.__str__() == 'None' or title.__str__() == 'None':
                continue

            title = title.group()

            #如果Q中有英文，一律删掉
            if re.search('[a-zA-Z]', title).__str__() != 'None':
                continue

            # print text
            answers = answer.group()
            answers = answers.split('}$${$(')



            #extract the best answer
            score = -1
            temp_score = 0.0

            best_answer = ''
            temp_answer = '太难回答了' #有的时候所有的答案都包括很多英文，不方便回答

            # 您好，请帮我删掉作品《钻石情人》${*$(已删除～～～～～～～～)$||1442943912}$2008-05-07 01:25:21
            # 这样的情况~按理说要删除，最后输出太难回答了

            # print "begin"
            for a in answers:
                 a = modify(a)

                 # 如果回答中有qq,QQ,比较长的英文,通通舍弃
                 if re.search('(qq)|(QQ)|(www)|WWW|(http)|(com)|([a-zA-Z]{5,}|'
                              '(已修改)|(已删除)|已处理|已通过)', a).__str__() != 'None':
                    continue

                 #如果回答长度超过150，直接删掉
                 if len(a) > 300:
                    temp_answer = '这个解释太长了'
                    continue

                 temp_score = score_comput(a)
                 if temp_score > score:
                    score = temp_score
                    best_answer = a

            #如果全是特殊匹配情况（不是太长就是带有网址），输出特殊匹配回答
            if best_answer == '':
                # best_answer = temp_answer
                continue

            #数据归一化,删除重复出现的(! ~ 。，-)
            title2 = norma(title)
            best_answer2 = norma(best_answer)

            #将当前行的信息写入到新的文件页
            f.write(title2)
            f.write('\t')
            # f.write(title_content[0])
            # f.write('\t')
            # f.write(answers[0])
            f.write(best_answer2)
            f.write('\n')

            # print(title[0] + ',' + title_content[0] + ',' + answers[0])


        f.close()
        print('\n--------------'+str(i)+'.txt'+'\n--------------')

# f.close()


print "end"