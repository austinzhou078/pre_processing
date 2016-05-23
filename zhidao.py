# -*- coding:utf-8 -*-
__author__ = 'Austin'

import re
import os
import os.path
import time

rootdir = "/Users/Austin/360云盘/论文/test/zhidao"

#分数计算函数
#  还有台湾的威盛，但是市场占有率很低还有苹果的CPU~~~~（叫什么名字了呢？）赛扬是低
# 端的奔腾)$||zan:0||gradeIndex:"7"||isFamous:"0"||isMaster:"0"||goodRate:"20"

def norma(text):
    text2 = re.sub('(\!|\~|\～|\。|\,|\-|\?|\·){2,}',' ',text)
    return text2

def score_comput(ans):

    # print ans
    zan = re.search('(?<=zan:)[0-9]*(?=\|\|gradeIndex)', ans).group()
    # gradeIndex = re.search('(?<=gradeIndex:\").*(?=\"\|\|isFamous)', ans).group()

    isFamous = re.search('(?<=isFamous:\")[0-9]*(?=\"\|\|isMaster)', ans).group()

    isMaster = re.search('(?<=isMaster:\")[0-9]*(?=\")', ans).group()

    # goodRate = re.search('(?<=goodRate:\").*(?=\")', ans).group()

    # length_weight = 1/len(ans)

    # disagree = re.search('(?<=disagree:).*', ans).group()



    if zan == '':
        zan = 0
    else:
        zan = int(zan)

    # if gradeIndex == '':
    #     gradeIndex = 0
    # else:
    #     gradeIndex = int(gradeIndex)

    if isFamous == '':
        isFamous = 0
    else:
        isFamous = int(isFamous)

    if isMaster == '':
        isMaster = 0
    else:
        isMaster = int(isMaster)

    # if goodRate == '':
    #     goodRate = 0
    # else:
    #     goodRate = int(goodRate)

    return zan + 2*isFamous + 2*isMaster

def modify(ans):
    if ans == '这个解释太长了' or ans == '自己百度去吧':
        return ans
    else:
        # print ans
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

            title = re.search('.*(?=\$\{\*)', text)

            answer = re.search('(?<=\$\{\*\$\().*(?=\$2)', text)

            if answer.__str__() == 'None' or title.__str__() == 'None':
                continue

            title = title.group()

            #将content部分删掉
            title = re.sub("\$\[<.*\]\$", '', title)

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

            #把不同答案之间区分开来
            answers = answer.group()
            answers = answers.split('}$${$(')


            #extract the best answer
            score = -1
            temp_score = 0.0

            best_answer = ''

            for a in answers: #这里的逻辑有点复杂
                if re.search('(www\.)|(http\:\/\/)', a).__str__() != 'None':
                    temp_answer = '自己百度去吧'
                    continue

                # 如果回答长度超过150，直接删掉
                if len(a) > 500:
                    temp_answer = '这个解释太长了'
                    continue

                #如果不是空洞内容的情况，计算分值
                temp_score = score_comput(a)
                if temp_score > score:
                    score = temp_score
                    best_answer = a

                 # # 判断当前答案分数是否超过最高分数
                 #    temp_score = score_comput(a)
                 #    if temp_score > score:
                 #        score = temp_score
                 #        best_answer = a
                 #
                 #        if re.search('(www\.)|(http\:\/\/)', a).__str__() != 'None':
                 #            best_answer = '自己百度去吧'
                 #            break
                 #
                 #        # 如果回答长度超过150，直接删掉
                 #        if len(a) > 500:
                 #            best_answer = '这个解释太长了'
                 #            break



                # # 如果回复里面包括网站信息，输出特殊回答,直接略过
                # if re.search('(www\.)|(http\:\/\/)', a).__str__() != 'None':
                #     temp_answer = '自己百度去吧'
                #     break
                # # 如果回答长度超过150，直接删掉
                # elif len(a) > 500:
                #     temp_answer = '这个解释太长了'
                #     break
                # else:
                #     # 判断当前答案分数是否超过最高分数
                #     temp_score = score_comput(a)
                #     if temp_score > score:
                #         score = temp_score
                #         best_answer = a

            #如果全是特殊匹配情况（不是太长就是带有网址），输出特殊匹配回答
            if best_answer == '':
                best_answer = temp_answer
            else:
                best_answer = modify(best_answer)

            #数据归一化,删除重复出现的(! ~ 。，-)
            title2 = norma(title)
            best_answer2 = norma(best_answer)
            print best_answer

            #将当前行的信息写入到新的文件页
            f.write(title2)
            f.write('\t')
            # f.write(title_content[0])
            # f.write('\t')
            # f.write(answers[0])
            # print(best_answer)
            f.write(best_answer2)
            f.write('\n')

            # print(title[0] + ',' + title_content[0] + ',' + answers[0])


        f.close()
        print('\n--------------'+str(i)+'.txt'+'\n--------------')


print "end"