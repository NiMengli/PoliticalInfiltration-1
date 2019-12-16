### 在这里将get_aggs函数进行拆分，这里只放活动信息统计的部分，该文件不会直接执行，会在profile_cal_main.py里统一调用进行计算。

### 标记好这个统计函数的输入与输出，以便于代码查看


import sys
import os
import time
import datetime
from pandas import DataFrame

sys.path.append("../../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'PoliticalInfiltration.settings'


# 获取单个用户的活动特征，输入数据格式为{uid1:[{},{}],uid2:[{},{}]},返回格式{timestamp_uid:{},timestamp_uid2:{}}
def get_msg_type_aggs(data_dict):
    user_behavior_dict = {}
    for uid in data_dict:
        mid_dict_list = data_dict[uid]
        df = DataFrame(mid_dict_list)
        behavior_dict = get_msg_aggs(df)
        behavior_dict["timestamp"] = int(time.time())
        behavior_dict["uid"] = uid
        behavior_dict["store_date"] = datetime.date.today()
        user_behavior_dict["%s_%s" % (str(behavior_dict["timestamp"]), uid)] = behavior_dict

    return user_behavior_dict


# 获取单个用户的活动特征，输入数据为pandas的df
def get_msg_aggs(df):
    behavior_dict = {}
    res_dict = df.groupby(df["message_type"]).size().to_dict()
    for k, v in res_dict.items():
        if k == 1:
            behavior_dict["originalnum"] = v
        elif k == 2:
            behavior_dict["commentnum"] = v
        elif k == 3:
            behavior_dict["retweetnum"] = v
    if len(behavior_dict) != 3:
        for k in ["originalnum", "commentnum", "retweetnum"]:
            if k not in behavior_dict:
                behavior_dict[k] = 0
    return behavior_dict
