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
def norma(text):
    text2 = re.sub('(\!|\！|`|\~|\～|\。|\,|\.|\-|\?|\？|\·){2,}',' ',text)
    return text2

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

#TODO 做一些修改在这里
def modify(ans):
     # print "ans: " + ans

    # print ans
     if ans == '这个解释太长了' or ans == '太难回答了':
            return ans
     else:
            # print "\n\n"
            # print ans
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
            # print "text is: "+text

            #如果有回答特别长，说明这个问题太宽泛了
            # if len(text) > 7000:
            #     continue


            #删除多余部分来去的title
            title = re.sub('(?=(\$\|)|(\$)).*(?=\n)', '', text)
            title = re.sub('\n', '', title)

            answer = re.search('(?<=\$\{\*\$\().*(?=\$2)', text)

            # print "title is " + title


            #如果Q 或者A 有空， 直接舍弃
            if answer.__str__() == 'None':
                continue

            #如果Q中有英文，一律删掉
            if re.search('[a-zA-Z]', title).__str__() != 'None':
                continue


            # print text
            answers = answer.group()

            # print "answer is " + answers



            answers = answers.split('}$${*$(')

            #extract the best answer
            score = -1
            temp_score = 0.0


            best_answer = ''
            temp_answer = '太难回答了' #有的时候所有的答案都包括很多英文，不方便回答

            # print "begin"
            for a in answers:
                # print a
                # print modify(a)

                # 如果回答中有qq,QQ,比较长的英文,通通舍弃
                if re.search('(qq)|(QQ)|(www)|WWW|(http)|(com)|([a-zA-Z]{5,})', modify(a)).__str__() != 'None':
                    continue

                    # 如果回答长度超过150，直接删掉
                if len(a) > 300:
                    temp_answer = '这个解释太长了'
                    continue

                temp_score = score_comput(a)
                if temp_score > score:
                    score = temp_score
                    best_answer = a

            # print "best_answer is :"+best_answer
            #如果全是特殊匹配情况（不是太长就是带有网址），输出特殊匹配回答
            if best_answer == '':
                best_answer = temp_answer
            else:
                best_answer = modify(best_answer)

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
        # print('\n--------------'+str(i)+'.txt'+'\n--------------')

# f.close()


print "end"