# -*- coding:utf-8 -*-
__author__ = 'Austin'

import re
import os
import os.path
import time

rootdir = "/Users/Austin/360云盘/论文/test/soso"

#分数计算函数
# (死马海马木马)$||solvedNum:0||notSolvedNum:220||originalNum:0||notOriginalNum:0}
# (木马.)$||solvedNum:0||notSolvedNum:0||originalNum:0||notOriginalNum:0}
# (木马)$}
# (木马、飞马)$}
# (才出生的马)$}
# (飞马)$}

def score_comput(ans):

    # print ans
    solvedNum = re.search('(?<=solvedNum:)[0-9]*', ans)
    notSolvedNum = re.search('(?<=notSolvedNum:)[0-9]*', ans)

    if solvedNum.__str__() == 'None':
        solvedNum = 0
    else:
        solvedNum = solvedNum.group()

    if notSolvedNum.__str__() == 'None':
        notSolvedNum = 0
    else:
        notSolvedNum = notSolvedNum.group()

    return int(solvedNum) + 0.5*int(notSolvedNum)

def modify(ans):
    # print ans
    return re.search('.*(?=\)\$)', ans).group()

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
        file = str(os.path.join(parent, filename)) #输出文件路径信息
        l = open(str(file), 'r')

        #当前目录下新建一个文件来存放筛选出来的数据,用数字1-n表示
        new_dir = parent
        new_dir += "/result/"
        new_dir += str(i)
        i += 1
        new_dir += ".txt"


        f = open(new_dir, 'w')


        for text in l:  #同一个file中的每一句话

            #如果有回答特别长，说明这个问题太宽泛了
            # if len(text) > 7000:
            #     continue

            # print text
            answer = re.search('(?<=\$\{\*\$\().*(?=\$2)', text)


            # print "----------"
            # print text
            #删除多余部分来去的title
            title = re.sub('(?=(\$\|)|(\$)).*(?=\n)', '', text)
            title = re.sub('\n', '', title)


            # print title
            # print "----------"

            if answer.__str__() == 'None' or title.__str__() == 'None':
                continue

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
            answers = answers.split('$${*$')



            #extract the best answer
            score = -1
            temp_score = 0.0

            for a in answers:

                if len(a) > 500:
                    break

                temp_score = score_comput(a)
                if temp_score > score:
                    score = temp_score
                    best_answer = a

            #将当前行的信息写入到新的文件页
            f.write(title)
            f.write('\t')
            # f.write(title_content[0])
            # f.write('\t')
            # f.write(answers[0])
            f.write(modify(best_answer))
            f.write('\n')

            # print(title[0] + ',' + title_content[0] + ',' + answers[0])


        f.close()
        print('\n--------------'+str(i)+'.txt'+'\n--------------')

# f.close()


print "end"