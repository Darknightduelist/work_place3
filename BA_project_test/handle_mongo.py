import random
import pymongo
from BA_project_test.A_clear_data import *
from BA_project_test.A_clear_data import relpace_Chinese, delete_same_str


class Mongo_client(object):
    def __init__(self):
        # 建立连接
        print("开始建立数据库连接......")
        self.myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        # 建立数据库
        self.mydb = self.myclient['weibo']
        # 创建一个数据表
        self.str0 = input("请输入数据表的名称(如果不命名则使用自动创建的名称)：")
        if self.str0 == '':
            r = random.randint(1, 1000000)
            db_name = str(r)
            self.mycollection = self.mydb['collection_weibo' + db_name]
            self.mycollection2 = self.mydb['collection_weibo' + db_name + '-other']
        else:
            self.mycollection = self.mydb[self.str0]
            self.mycollection2 = self.mydb[self.str0 + '-other']
        print("操作成功！")

    def insert_db(self,item):
        print("开始插入数据......")
        try:
            self.mycollection.insert_many(item)  # item是一个数组[]
        except TypeError:
            pass

    def insert_db2(self,item):
        print("开始插入数据......")
        try:
            self.mycollection2.insert_many(item)  # item是一个数组[]
        except TypeError:
            pass

    def get_input_name(self):
        return '#'+str(self.str0)+'#'

    # def get_collection_name(self):
    #     result = self.mycollection.list_collection_names(session=None)
    #     return result

    def select_all(self):
        try:
            if self.mycollection.find().count() == 0:
                print("该数据库元素为空！")
            else:
                flag = 0
                list = []
                for i in self.mycollection.find():
                    flag += 1
                    # print("第{0}个元素为：{1}".format(flag,i))
                    list.append(i)
                return list
            print("数组返回成功！")
        except:
            print("查询出错了！")

    def select_hot(self):
        try:
            if self.mycollection2.find().count() == 0:
                print("热门评论数据库元素为空！")
            else:
                flag = 0
                list = []
                agree_num = []
                all_count = 0
                for i in self.mycollection2.find():
                    if all_count > 10:
                        break
                    all_count += 1
                    flag += 1
                    tmp = i['hot_comment_agree_number']
                    agree_num.append(tmp)
                    jishu = 0
                    for j in agree_num:
                        if tmp == j:
                            jishu += 1
                        if jishu > 1:
                            break
                    if jishu > 1:
                        continue
                    # print("第{0}个元素为：{1}".format(flag,i))
                    list.append(i)
                return list
            print("热门评论数组返回成功！")
        except:
            print("热门评论查询出错了！")

    def get_clear_data(self,ss):
        list1 = []
        for i in self.select_all():
            str1 = delete_same_str(i.get('content'), ss)
            str2 = relpace_Chinese(str1)
            list1.append(str2)
        return list1

    def close_db(self):
        try:
            self.myclient.close()
            print("数据库关闭成功！")
        except:
            print("数据库关闭失败！")


operate_data = Mongo_client()


# if __name__ == '__main__':
#     t = Mongo_client()
#     print(t.select_hot())
