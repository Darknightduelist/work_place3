from BA_project_test.handle_mongo import operate_data
from BA_project_test.A_clear_data import *


def single_get_data():
    t_list = operate_data.select_all()
    # operate_data.close_db()
    return t_list


def single_get_hot_data():
    t_list = operate_data.select_hot()
    # operate_data.close_db()
    return t_list


def flask_word_count(ss):  # ok
    counts = {}
    list_word_cloud = []  # 为了使用词云准备的
    # ***********************************************************
    t_list = single_get_data()
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
    # ***********************************************************
    list0 = format_data_list  # 里面是评论内容的数组
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
    # ///////////////////////////////////////////////////////////
    list8 = items  # list8是一个元组数组
    data_dic = [{"name": x[0], "value": x[1]} for x in list8]
    name_list = [name['name'] for name in data_dic]
    value_list = [value['value'] for value in data_dic]
    info1 = {}
    info1['x_name'] = name_list
    info1['x_value'] = value_list
    return info1  # 这个是一个集合


def data_map():  # ok
    t_list2 = single_get_data()
    format_data_list2 = []
    for i in t_list2:
        format_data_list2.append(i.get('map_position'))
    counts2 = {}
    for position in format_data_list2:
        if len(position) == 1:
            continue
        elif position == '其它' or position == '海外':
            continue
        else:
            counts2[position] = counts2.get(position, 0) + 1
    items2 = list(counts2.items())
    items2.sort(key=lambda x: x[1], reverse=True)
    list9 = items2  # list8是一个元组数组
    data_dic2 = [{"position": x[0], "value": x[1]} for x in list9]
    name_list2 = [name['position'] for name in data_dic2]
    value_list2 = [value['value'] for value in data_dic2]
    info2 = {}
    info2['x_position'] = name_list2
    info2['x_value'] = value_list2
    return info2  # 这个是一个集合


def test_hot():  # 可以进行一下排序操作
    list3 = single_get_hot_data()
    hot_comment_list = [comment['hot_comment_info'] for comment in list3]
    hot_agree_list = [agreement['hot_comment_agree_number'] for agreement in list3]
    info3 = {}
    info3['x_hot_comment'] = hot_comment_list
    info3['x_hot_agree'] = hot_agree_list
    return info3


def get_hot_comment():  # 已经进行了排序 ok
    list3 = single_get_hot_data()
    hot_comment_list = [comment['hot_comment_info'] for comment in list3]
    hot_agree_list = [agreement['hot_comment_agree_number'] for agreement in list3]
    counts = {}
    tag = 0
    for i in hot_comment_list:
        counts[str(i)] = int(hot_agree_list[tag])
        tag += 1
    items3 = list(counts.items())
    items3.sort(key=lambda x: x[1], reverse=False)
    hot_comment_list2 = [comment2[0] for comment2 in items3]
    hot_agree_list2 = [agreement2[1] for agreement2 in items3]
    info3 = {}
    info3['x_hot_comment'] = hot_comment_list2
    info3['x_hot_agree'] = hot_agree_list2
    return info3


def is_china_province(pro):
    province = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江",
                "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
                "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾",
                "内蒙古", "广西", "西藏", "宁夏", "新疆", "北京", "天津", "上海",
                "重庆", "香港", "澳门"]
    if pro in province:
        return True
    return False


def get_overseas_portion():
    list4 = single_get_data()
    counts = {'中国': 0, '海外': 0, '其它': 0}
    for i in list4:
        t = is_china_province(i['map_position'])
        if i['map_position'] == '海外':
            counts['海外'] += 1
        elif i['map_position'] == '其它':
            counts['其它'] += 1
        elif t:
            counts['中国'] += 1
        elif i['map_position'] == '无':
            continue
        else:
            counts['海外'] += 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    data_dic2 = [{"is_overseas": x[0], "value": x[1]} for x in items]
    provinces_list2 = [name['is_overseas'] for name in data_dic2]
    value_list2 = [value['value'] for value in data_dic2]
    info2 = {}
    info2['x_overseas'] = provinces_list2
    info2['x_values'] = value_list2
    return info2  # 这个是一个集合


def get_data_sum():
    pass


# if __name__ == '__main__':
#     print(get_overseas_portion())
# #     # t = flask_word_cloud()
# #     # print(t['x_name'])
# #     # print(t['x_value'])
