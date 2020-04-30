def get_position(arr):
    province = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江",
                "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
                "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾",
                "内蒙古", "广西", "西藏", "宁夏", "新疆", "北京", "天津", "上海",
                "重庆", "香港", "澳门", "其它", "海外"]
    for i in arr:
        t = i.replace(u'\xa0', u'')
        for j in province:
            if j in t:
                return j
    return '其它'
