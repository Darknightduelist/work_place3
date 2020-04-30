# from BA_project_test.handle_mongo import Mongo_client

import re
import jieba
import wordcloud
"""
这是一个生成词云的py文件
"""


def get_number(string):
    number = re.findall('\d+', string)
    if number:
        return number[0]
    else:
        return -1


def half_url_comment(url):
    s = 'https://weibo.cn'
    t = ''
    if s in url:
        t = url.replace(s, '')
    return t


def find_url(string):
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
    return url


def relpace_Chinese(words):
    for ch in words:
        if '\u4e00' <= ch <= '\u9fff':  # or ch.isalnum(): # 后面的这个判断是不是字母或者是数字
            continue
        else:
            words = words.replace(ch, '')
    return words


def delete_same_str(s1, s2):  # s1是主串，s2是子串
    flag0 = 1
    while flag0 == 1:  # 若无子字符串在内则跳出循环
        flag0 = 0
        if s2 in s1:
            s1 = s1.replace(s2, '')
            flag0 = 1
    return s1


# 并不涉及插入操作
def update_clear_data(ss):
    # tt = Mongo_client()
    from BA_project_test.handle_mongo import operate_data
    t_list = operate_data.select_all()
    # ss = input("请输入要搜索的话题(模拟):")
    s_add = '#' + ss + '#'
    flag = 0
    format_data_list = []  # 用于处理返回后的数据的一个数组
    for i in t_list:
        # print(i.get('content'))
        flag += 1
        str1 = delete_same_str(i.get('content'), s_add)
        # print("原装--这是第{0}条，内容：{1}".format(flag, str1))
        str2 = relpace_Chinese(str1)
        format_data_list.append(str2)
        # print("修正--这是第{0}条，内容：{1}".format(flag, str2))
    operate_data.close_db()
    return format_data_list


def jieba_word_count(ss):
    counts = {}
    list_word_cloud = []  # 为了使用词云准备的
    list0 = update_clear_data(ss)
    for i in list0:
        words = jieba.lcut(i)
        for word in words:
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word,0) + 1
                list_word_cloud.append(word)
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(15):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word, count))
    txt = " ".join(list_word_cloud)
    return txt


def word_cloud_generate(ss):  # 传入的ss只是搜索的内容，用于生成图片的名称
    tt = jieba_word_count(ss)
    w = wordcloud.WordCloud(font_path="msyh.ttc", width=1000, height=700, background_color="white",collocations=False)  # font_path字体,最后一个参数极其重要
    w.generate(tt)
    file_name = str(ss)+".png"
    w.to_file(file_name)
    print("词云生成成功！")




