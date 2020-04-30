from BA_project_test.handle_mongo import operate_data
from BA_project_test.A_clear_data import *


def flask_word_count(str_input):
    counts = {}
    list_word_cloud = []  # 为了使用词云准备的
    list0 = update_clear_data(str_input)
    for i in list0:
        words = jieba.lcut(i)
        for word in words:
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
                list_word_cloud.append(word)
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items


def flask_word_cloud():
    list8 = flask_word_count('意大利违反隔离规定或被判21年')  # list8是一个元组数组
    data_dic = [{"name": x[0], "value": x[1]} for x in list8]
    name_list = [name['name'] for name in data_dic]
    info1 = {}
    info1['x_name'] = name_list
    info1['data'] = data_dic
    return info1

#
# if __name__ == '__main__':
#
#     print(flask_word_cloud())

