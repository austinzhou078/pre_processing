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


def score_comput(ans):

    ans2 = re.search('.*(?=\)\$\|)', ans).group()
    l = len(ans2)
    score = abs(l-50)

    return (ans2, score)

#     return 1/len(ans)
#
# def modify(ans):
#     return re.search('.*(?=\)\$\|\|)', ans).group()

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

            # #如果有回答特别长，说明这个问题太宽泛了,删！
            # if len(text) > 7000:
            #     continue

            # print text
            title = re.search('.*(?=\$\{\*)', text)

            answer = re.search('(?<=\$\{\*\$\().*(?=\$2)', text)

            if answer.__str__() == 'None' or title.__str__() == 'None':
                continue

            title = title.group()

            # #将content部分删掉
            # title = re.sub("\$\[<.*\]\$", '', title)


            # print "------------\nbegining"
            # print time.time()

            # print title
            #如果没人回答的话就直接跳过
            # if len(answer) == 0 or len(title) == 0:
            #     continue

            # if answer == '' or title == '':
            #     continue


            # print time.time()
            # print "ending\n------------"

            # print text
            answers = answer.group()
            answers = answers.split('}$${$(')



            #extract the best answer
            score = -1
            temp_score = 0.0

            for a in answers:
                if len(a) > 500:
                    break

                (aa, temp_score) = score_comput(a)

                if temp_score > score:
                    score = temp_score
                    best_answer = aa

            #将当前行的信息写入到新的文件页
            f.write(title)
            f.write('\t')
            # f.write(title_content[0])
            # f.write('\t')
            # f.write(answers[0])
            f.write(best_answer)
            f.write('\n')

            # print(title[0] + ',' + title_content[0] + ',' + answers[0])


        f.close()
        print('\n--------------'+str(i)+'.txt'+'\n--------------')

# f.close()


print "end"