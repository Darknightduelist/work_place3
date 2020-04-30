# -*- coding: utf-8 -*-
import threading
import BA_project_test.get_person_province
import BA_project_test.A_clear_data
from multiprocessing import Queue
import requests
import re
import time
from lxml import etree
from urllib import parse
import urllib
from BA_project_test.handle_mongo import operate_data
# from BA_project_test.handle_mongo import Mongo_client
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

# 我们定义两个全局的flag
data_flag = False
data_queue = Queue()
login_session = requests.session()
yeshu = 1


class Craw_page(object):
    """
    这个类的功能是将爬取的所有网页放到数据队列中去
    """
    # 重写父类
    sousou = ''
    global login_session

    def __init__(self, data_queue):
        # # 线程的名称
        # self.thread_name = thread_name
        # # 页码的队列
        # self.page_queue = page_queue
        # 数据的队列
        self.data_queue = data_queue
        self.headers0 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_T_WM=77738612877; SCF=AtmU1rw0l6cS8iAGDxLbor_ysreKCPWmafAwuwa43gweSsRk_V52rRKKobBrfpb8BGLbFQ3cvbeqv4BKS3C_HT4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWLBIy_2kNrJvDdJXXHhH7b5JpX5KzhUgL.Fo-NeKnf1Kzc1hz2dJLoIN-LxKnLBo-LBoMLxKBLBonLB-2LxKBLB.zL1h5LxKBLBo.L1hnLxK-L1K5L12BLxK-LB-BL1KMLxK-LBK-LB.BLxK-L1K2LBKzLxKnLB.qL1KnLxKqL1KnLB-qLxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMt; login=e5e8571d42ffdfe74d93d3d0cd37d474; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home; SUB=_2A25zYag7DeRhGeBP71IV9y7IzT-IHXVQrchzrDV6PUJbkdANLVfXkW1NRUptHodq7kcSx25zALAEY0SDBl70fPH5; SUHB=0d4-WcS-TeR6Yw; SSOLoginState=1583732843",
            "Host": "passport.weibo.cn",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.headers2 = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "238",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "_T_WM=77738612877; SCF=AtmU1rw0l6cS8iAGDxLbor_ysreKCPWmafAwuwa43gweSsRk_V52rRKKobBrfpb8BGLbFQ3cvbeqv4BKS3C_HT4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWLBIy_2kNrJvDdJXXHhH7b5JpX5KzhUgL.Fo-NeKnf1Kzc1hz2dJLoIN-LxKnLBo-LBoMLxKBLBonLB-2LxKBLB.zL1h5LxKBLBo.L1hnLxK-L1K5L12BLxK-LB-BL1KMLxK-LBK-LB.BLxK-L1K2LBKzLxKnLB.qL1KnLxKqL1KnLB-qLxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMt; login=e5e8571d42ffdfe74d93d3d0cd37d474; SUB=_2A25zYns_DeRhGeBP71IV9y7IzT-IHXVQrQV3rDV6PUJbkdANLXX1kW1NRUptHhhQl5-Lztv3Ai1Dw77HkG4A058p; SUHB=0ftpVKb2GYb2-1; SSOLoginState=1583745903",
            "Host": "passport.weibo.cn",
            "Origin": "https://passport.weibo.cn",
            "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F%3Fluicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home&backTitle=%CE%A2%B2%A9&vt=",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.headers3 = {
            "authority": "weibo.cn",
            "method": "GET",
            "path": "/?luicode=10000011&lfid=102803_ctg1_8999_-_ctg1_8999_home",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "_T_WM=77738612877; SCF=AtmU1rw0l6cS8iAGDxLbor_ysreKCPWmafAwuwa43gweSsRk_V52rRKKobBrfpb8BGLbFQ3cvbeqv4BKS3C_HT4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWLBIy_2kNrJvDdJXXHhH7b5JpX5KzhUgL.Fo-NeKnf1Kzc1hz2dJLoIN-LxKnLBo-LBoMLxKBLBonLB-2LxKBLB.zL1h5LxKBLBo.L1hnLxK-L1K5L12BLxK-LB-BL1KMLxK-LBK-LB.BLxK-L1K2LBKzLxKnLB.qL1KnLxKqL1KnLB-qLxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMt; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home; SUB=_2A25zYmHmDeRhGeBP71IV9y7IzT-IHXVQrQ-urDV6PUJbkdAKLW37kW1NRUptHoRrxmqAuk62uy5qgPvhAbTr-Zh-; SUHB=04WuDIqZU-E814; SSOLoginState=1583747510",
            "referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F%3Fluicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home&backTitle=%CE%A2%B2%A9&vt=",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

        self.params = {
            "entry": "mweibo",
            "r": "https://weibo.cn/?luicode=10000011&lfid=102803_ctg1_8999_-_ctg1_8999_home",
            "backTitle": "(unable to decode value)",
            "vt": ""
        }

        self.data = {
            "username": "17863976565",
            "password": "haoren357A",
            "savestate": "1",
            "r": "https://weibo.cn/?luicode=10000011&lfid=102803_ctg1_8999_-_ctg1_8999_home",
            "ec": "0",
            "pagerefer": "https://weibo.cn/pub/",
            "entry": "mweibo",
            "wentry": "",
            "loginfrom": "",
            "client_id": "",
            "code": "",
            "qq": "",
            "mainpageflag": "1",
            "hff": "",
            "hfp": ""
        }

    # 获取全部页数的函数
    def str_position(self, str0):
        str0 = str0.strip()
        length = len(str0)
        position = 0
        for i in str0:
            if i == '/':
                break
            position += 1
        return str0[position + 1:-1]

    def run(self):
        print("start!!!!!!")
        index_url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F%3Fluicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home&backTitle=%CE%A2%B2%A9&vt='
        login_url = 'https://passport.weibo.cn/signin/login'
        final_url = 'https://weibo.cn/?luicode=10000011&lfid=102803_ctg1_8999_-_ctg1_8999_home'
        # 最开始的登录页面
        # login_session = requests.session()
        index_response = login_session.get(url=index_url, headers=self.headers0)
        # 登录页面
        login_response = login_session.post(url=login_url, headers=self.headers2, data=self.data)
        # 登录后的微博主页
        final_response = login_session.get(url=final_url, headers=self.headers3)
        # 要搜索的url的链接,可以实现搜索话题的功能了
        sousou = input("请输入要搜索的话题：")
        header_sou = {
            "authority": "weibo.cn",
            "method": "GET",
            "path": "/search/mblog/?keyword=" + urllib.parse.quote(sousou),
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "_T_WM=77738612877; SCF=AtmU1rw0l6cS8iAGDxLbor_ysreKCPWmafAwuwa43gweSsRk_V52rRKKobBrfpb8BGLbFQ3cvbeqv4BKS3C_HT4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWLBIy_2kNrJvDdJXXHhH7b5JpX5KzhUgL.Fo-NeKnf1Kzc1hz2dJLoIN-LxKnLBo-LBoMLxKBLBonLB-2LxKBLB.zL1h5LxKBLBo.L1hnLxK-L1K5L12BLxK-LB-BL1KMLxK-LBK-LB.BLxK-L1K2LBKzLxKnLB.qL1KnLxKqL1KnLB-qLxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMt; SUB=_2A25zYmHmDeRhGeBP71IV9y7IzT-IHXVQrQ-urDV6PUJbkdAKLW37kW1NRUptHoRrxmqAuk62uy5qgPvhAbTr-Zh-; SUHB=04WuDIqZU-E814; SSOLoginState=1583747510; MLOGIN=1",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        sou_url = 'https://weibo.cn/search/mblog/?keyword=' + sousou
        sou_response = login_session.get(url=sou_url, headers=header_sou)
        weibo_html = etree.HTML(sou_response.text.encode('utf-8'))  # 改改改改改改改改改改改改改
        # # 获取微博条数
        # test = weibo_html.xpath("/html/body/div[6]/span/text()")
        # t = test[0]
        # print(t[1:-1])
        # 获取微博的页数
        test = weibo_html.xpath('//*[@id="pagelist"]/form/div/text()[2]')
        t = test[0]
        final_position = self.str_position(t)  # 微博的页数
        # print(type(final_position))
        global yeshu
        yeshu = int(final_position)
        # print(yeshu)
        for i in range(1, yeshu + 1):
            # https://weibo.cn/search/mblog?hideSearchFrame=&keyword=意大利违反隔离规定或被判21年&page=1
            page_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + str(sousou) + '&page=' + str(i)
            time.sleep(1)
            print('当前构造的url为：{0}'.format(page_url))
            # 请求当前构造的url
            sou_response = login_session.get(url=page_url, headers=header_sou, timeout=5)
            # sou_response.encoding = 'utf-8'
            # 将请求回来的网页文本数据放到数据队列里面去
            self.data_queue.put(sou_response.content.decode('utf-8'))
            # print(sou_response.text) # 测试样例完全正确****************
        print("数据队列的大小为：{0}".format(data_queue.qsize()))  # 这里可以插入数据到队列中去,到这里可以进行
        return sousou


# 处理网页文本数据类
class Crawl_html(object):
    global login_session

    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.person_header = {
            "authority": "weibo.cn",
            "method": "GET",
            "path": "/scvideo",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "SCF=AtmU1rw0l6cS8iAGDxLbor_ysreKCPWmafAwuwa43gweSsRk_V52rRKKobBrfpb8BGLbFQ3cvbeqv4BKS3C_HT4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWLBIy_2kNrJvDdJXXHhH7b5JpX5KzhUgL.Fo-NeKnf1Kzc1hz2dJLoIN-LxKnLBo-LBoMLxKBLBonLB-2LxKBLB.zL1h5LxKBLBo.L1hnLxK-L1K5L12BLxK-LB-BL1KMLxK-LBK-LB.BLxK-L1K2LBKzLxKnLB.qL1KnLxKqL1KnLB-qLxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMt; SUB=_2A25zYmHmDeRhGeBP71IV9y7IzT-IHXVQrQ-urDV6PUJbkdAKLW37kW1NRUptHoRrxmqAuk62uy5qgPvhAbTr-Zh-; SUHB=04WuDIqZU-E814; _T_WM=056a7eb45ad2495565f0535788cf655d",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }

    def run(self):
        i = 1
        # tmp = Mongo_client()
        while data_queue.qsize() != 0:
            text = self.data_queue.get()  # 当get队列为空时，就会抛出异常
            result = self.parse0(text)  # result是一个元组，里面包括两个返回值
            print("开始进行微博内容的数据写入......")
            operate_data.insert_db(result)  # ****************-+++++++++++++++++++++++++++++++++++++++++000000
            # print("开始进行微博评论的数据写入......")
            # operate_data.insert_db2(result[1])  # ****************-+++++++++++++++++++++++++++++++++++++++++000000
            print(result)
            # print(result[1])
            print("正在处理第" + str(i) + "页的xml数据")
            i = i + 1

    # 处理网页的方法,要修改的方法***************
    def parse0(self, text):
        # html实例化
        # print("这里可以执行到0")
        # print("text:"+text)
        try:
            html_t = etree.HTML(text.encode('utf-8'))
            # print("这里可以执行到0.001")  # 执行不到这里
            # ***************************************************************
            count = html_t.xpath('//a[@class="nk"]')
            list_length = len(count)
            print("当前的数组长度为：{}".format(list_length))
            str_xpath = '//div[@id][position()<=' + str(list_length) + ']'
            print(str_xpath)
            # ***************************************************************
            # all_div = html_t.xpath('//div[@id][position()<=9]')
            all_div = html_t.xpath(str(str_xpath))
            # print("这里可以执行到1")
            info_list = []
            # hot_comment_info = []
            for i in all_div:
                s3 = ''
                info_information = {}
                # 获取赞数所进行的正则表达式选取操作++++++++++++++++++++++++++++++++++++
                zan_result = etree.tostring(i, encoding="utf-8", pretty_print=True, method="html").decode('utf-8')
                # print(zan_result)
                try:
                    # 寻找赞数
                    pattern1 = re.compile(r"[\u8d5e][[](\d*?)[]]")
                    # 寻找转发数
                    pattern2 = re.compile(r"[\u8f6c][\u53d1][[](\d*?)[]]")
                    # 寻找评论数
                    pattern3 = re.compile(r"[\u8bc4][\u8bba][[](\d*?)[]]")
                    # #################################################### 更正
                    value11 = pattern1.findall(zan_result)
                    value22 = pattern2.findall(zan_result)
                    value33 = pattern3.findall(zan_result)
                    if len(value11) == 1:
                        s1 = value11[0]
                    else:
                        s1 = value11[-1]
                    if len(value22) == 1:
                        s2 = value22[0]
                    else:
                        s2 = value22[-1]
                    if len(value33) == 1:
                        s3 = value33[0]
                    else:
                        s3 = value33[-1]
                    print("赞数：{0}  转发数：{1}  评论数：{2}".format(s1, s2, s3))
                    info_information['agree_number'] = s1
                    info_information['forward_number'] = s2
                    info_information['comment_number'] = s3
                except:
                    print("未找到！")
                    info_information['agree_number'] = -1
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # xpath返回的是列表，所以要获取列表中索引为0的数据
                info_information['name'] = i.xpath('.//a[@class="nk"]/text()')[0]
                # print(info_information['name'])
                tt = i.xpath('.//span[@class="ctt"]')
                info_information['content'] = tt[0].xpath("string(.)")
                info_information['time'] = i.xpath('//span[@class="ct"]/text()')[0]
                # 下面的是关于获取用户地址信息的---------------------------------
                try:
                    person_href = i.xpath('.//div/a[@class="nk"]/@href')[0]
                    info_information['person_href'] = person_href
                    info_url = str(person_href)
                    person_response1 = login_session.get(url=info_url, headers=self.person_header, timeout=5)
                    time.sleep(0.5)
                    if person_response1.status_code != 200:
                        person_response1 = login_session.get(url=info_url, headers=self.person_header, timeout=5)
                        time.sleep(0.5)
                    person_response1.encoding = 'utf-8'  # #####################
                    ss = person_response1.content.decode('utf-8')  # ####################
                    html_person = etree.HTML(ss.encode('utf-8'))
                    person_info1 = html_person.xpath('//div[@class="ut"]/span[@class="ctt"]/text()')
                    person_info2 = BA_project_test.get_person_province.get_position(person_info1)
                    # print("用户地址信息:{}".format(person_info2))
                    info_information['map_position'] = person_info2
                except AttributeError:
                    print("地址未找到！")
                    info_information['map_position'] = '无'
                # -------------------------------------------------------获取网友评论

                try:
                    if int(s3) > 200:

                        comment_href = i.xpath('.//div/a[@class="cc"]/@href')[0]
                        comment_url = str(comment_href)
                        string = BA_project_test.A_clear_data.half_url_comment(comment_url)
                        comment_header = {
                            "authority": "weibo.cn",
                            "method": "GET",
                            "path": string,
                            "scheme": "https",
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                            "accept-encoding": "gzip, deflate, br",
                            "accept-language": "zh-CN,zh;q=0.9",
                            "cookie": "_T_WM=43879101262; SCF=Ai_XZtw0KpjErh4Lk_DF8nkQrZjvJlXYLSa1RbCIzD4vAwKlJNu7uQiU_OoHb3GsQNgyrd8lxawS5EiNeyujwI0.; SUB=_2A25zlq3ADeRhGeBP71IV9y7IzT-IHXVReDOIrDV6PUJbkdAKLXChkW1NRUptHmdGER475m1l2xvphf7D7NveXC-Y; SUHB=0cSniCqGytZA2_",
                            "referer": "https://weibo.cn/search/?pos=search",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "same-origin",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

                        }
                        comment_response = login_session.get(url=comment_url, headers=comment_header, timeout=5)
                        time.sleep(1.5)
                        comment_response.encoding = 'utf-8'
                        cc = comment_response.content.decode('utf-8')
                        html_comment = etree.HTML(cc.encode('utf-8'))
                        # 获取热评
                        comment_info = html_comment.xpath('//div[@class="c"and@id!="M_"][position()<=2]/span[@class="ctt"]/text()')
                        # 获取热评用户名
                        comment_username = html_comment.xpath('//div[@class="c"and@id!="M_"][position()<=2]/span[@class="kt"]/following-sibling::a[1]/text()')
                        # 获取热评获赞数
                        comment_agree_number = html_comment.xpath('//div[@class="c"and@id!="M_"][position()<=2]/span[@class="cc"][1]/a/text()')
                        # ############ 这里需要进行插入到一个新的数据库里面去 ################ 别忘记了写
                        hot_comment_info = []
                        for k in range(2):
                            hot_set = {}
                            hot_set['hot_comment_username'] = comment_username[k]
                            hot_set['hot_comment_info'] = comment_info[k]
                            hot_set['hot_comment_agree_number'] = BA_project_test.A_clear_data.get_number(comment_agree_number[k])
                            hot_comment_info.append(hot_set)
                        print("*****开始进行微博热门评论的数据写入*****")
                        operate_data.insert_db2(hot_comment_info)
                        print(hot_comment_info)
                        # print(comment_info)
                        # print(comment_username)
                        # print(comment_agree_number)
                    else:
                        pass
                except:
                    print("访问热评失败！")
                    # info_information['comment_content'] = '失败!'
                # --------------------------------------------------------
                info_list.append(info_information)
            return info_list
        except IndexError:
            pass


def test_queue(data_queue):
    try:
        while data_queue.qsize() != 0:
            print(data_queue.get(block=False))
    except:
        print("队列已空")


def main():
    global data_queue
    t = Craw_page(data_queue)
    sou = t.run()  # 可以获取到要搜索标题
    c = Crawl_html(data_queue)
    c.run()
    print('开始生成词云......')
    time.sleep(3)
    BA_project_test.A_clear_data.word_cloud_generate(sou)


# if __name__ == '__main__':
#     print('yes')