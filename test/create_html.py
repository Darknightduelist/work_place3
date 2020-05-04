from pyecharts import WordCloud, Pie, Bar
from test.get_data_test import *


def create_wordcloud():  # 生成词云ok
    t = flask_word_count()
    name = t['x_name']
    value = t['x_value']
    wordcloud1 = WordCloud("微博词云图")  # , width=1300, height=620)
    wordcloud1.add("", name, value, word_size_range=[10, 100])
    # wordcloud1.show_config()
    wordcloud1.render(path="微博内容分词结果.html")


def create_map():  # 生成地图OK
    from pyecharts import Geo
    from pyecharts import Map
    t = data_map()
    position = t['x_position']
    count = t['x_value']
    map = Map("地域分布", width=1200, height=600)
    map.add("", position, count, visual_range=[0, 50], maptype='china',
            is_visualmap=True, visual_text_color='#000', is_label_show=True)
    map.render(path="微博发布者所在区域.html")
    # print(position)


def create_pie():  # 关于国内，其它，海外的饼图 ok
    tmp = get_overseas_portion()
    attr = tmp['x_overseas']
    v1 = tmp['x_values']
    pie = Pie("海内外比例")
    pie.add("", attr, v1, radius=[15, 75], is_label_show=True)
    # pie.show_config()  # 会在控制台输出代码
    pie.render(path="海内外用户分布饼图.html")


def create_bar():  # 横着的柱状图,关于中国省份的热门评论 ok
    list3 = get_hot_comment()
    comment_hot = list3['x_hot_comment']
    agree_hot = list3['x_hot_agree']
    # print(comment_hot)
    # print(agree_hot)
    bar = Bar("微博热门评论")
    bar.add("网友评论", comment_hot, agree_hot, is_convert=True)
    # bar.show_config()  # 会在控制台输出代码
    bar.render(path="热门评论水平条形图.html")


def get_all_div():
    create_wordcloud()
    create_map()
    create_pie()
    create_bar()


if __name__ == '__main__':
    get_all_div()



