import csv
import json
import os, sys
import ctypes
import requests
from gevent import monkey

monkey.patch_all()

import sqlite3
from functools import wraps
import threading
import time
import datetime
from math import sqrt, log
import numpy as np
from math import *
import pymongo
import pymysql
from signalr import Connection
from requests import Session
from datetime import timedelta

import settings

"""

"""
class ProcessData(threading.Thread):
    def __init__(self):
        super().__init__()

        self.dic = {}
        self.last_transform_time = self.now
        self.vibData_cache = []
        self.raw_vibData_cache = []
        self.processed_raw_vibData = []
        self.load_cache = []
        self.pre_data = None
        self.user_settings = {}
        self.set_feed = 0
        self.set_speed = 0
        self.tool_num = 0
        self.load = 0
        self.tool_hp = 0
        self.tool_hp_pre = 1
        self.s = requests.Session()
        self.companyNo = "CMP20210119001"
        self.deviceNo = "0001"
    @property
    def now(self):
        return datetime.datetime.now()

    @property
    def now_str(self):
        return self.now.strftime(settings.DATETIME_PATTERN)

    def clothes(blanking_time, flag=False):
        """
        限制函数的执行间隔
        参数 blanking_time: 间隔时间
            flag: 如果为True 将在指定时间后执行 否则立马执行
        """
        def decorate(func):
            @wraps(func)
            def ware(self, *args, **kwargs):
                last_time = self.dic.get(func)

                if not last_time:
                    ret = None
                    if not flag:
                        ret = func(self, *args, **kwargs)
                    self.dic[func] = self.now
                    return ret
                elif (self.now - last_time) >= timedelta(milliseconds=blanking_time):
                    self.dic[func] = self.now
                    return func(self, *args, **kwargs)
            return ware
        return decorate

    def setup(self):
        print("正在准备中。。。")
        try:
            self.get_mangodb_connect()
            # self.get_mysql_connect()
            self.get_signalr_hub()
            self.set_machineinfo_from_file()
            self.ready = True
        except Exception as e:
            print(e)
            self.ready = False

    def get_mangodb_connect(self):
        """
        获取mongodb连接
        """
        self.mangodb_connect = pymongo.MongoClient(settings.mangodb_info['host'], serverSelectionTimeoutMS=settings.mangodb_info['connect_timeoutMS'])
        dblist = self.mangodb_connect.list_database_names()

    def get_mysql_connect(self):
        """
        获取上传刀具健康度的mysql连接
        """
        self.mysql_connect = pymysql.connect(**settings.hp_mysql_info)
        self.cursor = self.mysql_connect.cursor()

    def get_signalr_hub(self):
        """
        获取websocket连接
        """
        self.session = Session()
        self.connection = Connection(settings.signalr_hub_info['url'], self.session)
        self.hub = self.connection.register_hub(settings.signalr_hub_info["name"])
        self.connection.start()

    @clothes(settings.VIBDATA_DB_GET_BLANKING_TIME)
    def prepare_vibrationData(self):
        """
        每个一秒钟从数据库中获取一次振动数据并处理成相应格式
        """
        origin_data = self.get_origin_vibrationData()
        #print(origin_data)
        self.process_vibrationData(origin_data)
        self.make_vibDate_cache()

    def get_origin_vibrationData(self, limit=settings.VIBDATA_COUNT):
        """
        从数据库中获得原始数据
        """
        cols = self.mangodb_connect["VibrationData"][settings.mangodb_info["tb_name"]].find({}, sort=[('_id', pymongo.DESCENDING)],
                                                                      limit=limit)
        return list(cols)[::-1]

    def process_vibrationData(self, db_data):
        """
        把数据库请求得到的数据处理成对应结果
        通过self.pre_data存放
        """
        data = []
        for item in db_data:
            data.extend(item['zdata'])
        data = [x+50 for x in data]
        self.pre_data = data
        return data

    @clothes(settings.LOADDATA_DB_GET_BLANKING_TIME)
    def prepare_machineInfo(self):

        origin_machineinfo = self.get_origin_machineinfo()
        self.set_machineinfo(origin_machineinfo)
        if self.tool_num not in self.user_settings.keys():
            print("用户还未设定当前刀具信息")
            raise Exception
        self.make_load_cache()

    def make_load_cache(self):
        self.load_cache.append(self.load)

    @clothes(settings.LOADDATA_UPLOAD_BLANKING_TIME, flag=True)
    def 发送负载数据到云端(self):
        print("发送负载到云端%s"%self.load_cache)
        self.put_loaddata_to_cloud(self.load_cache)
        self.load_cache = []
        
    def put_loaddata_to_cloud(self, data):
        """
        发送负载数据到云端 通过websocket
        :param data:
        :return:
        """
        data = ",".join([str(i) for i in data])
        try:
            self.hub.server.invoke("broadcastDJJK_Working", self.companyNo, self.deviceNo, self.now_str, data)
        except Exception as e:
            print(e)
            self.ready = False

    def get_origin_machineinfo(self):
        """
        获得机台状态信息
        SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM, ACT_FEED, ACT_SPEED
        :return:
        """
        con = sqlite3.connect(settings.MACHINEINFO_DB_PATH)
        cur = con.cursor()

        cur.execute(settings.SQLITE_SQL)
        ret = cur.fetchone()
        set_feed = ret[1]
        act_feed = ret[4]
        set_speed = ret[2]
        act_speed = ret[5]
        load = ret[0]
        tool_num = ret[3]

        if tool_num < 10:
            tool_num = "T0" + str(tool_num)
        else:
            tool_num = "T" + str(tool_num)
        return {"set_feed": set_feed, "act_feed": act_feed, "set_speed": set_speed,"act_speed": act_speed, "tool_num":tool_num, 'load':load}

    def set_machineinfo(self, origin_machineinfo):
        """
        设定算法所需的机台状态信息
        :param origin_machineinfo:
        :return:
        """
        self.set_feed = origin_machineinfo["set_feed"]
        self.act_feed = origin_machineinfo["act_feed"]
        self.set_speed = origin_machineinfo["set_speed"]
        self.act_speed = origin_machineinfo["act_speed"]
        self.tool_num = origin_machineinfo["tool_num"]
        self.load = origin_machineinfo["load"]

    def read_user_settings(self):
        """
        通过本地表格文件读取用户设定,
        读取出来的数据均为字符串
        :return:
        """
        #print(settings.SHEET_PATH)
        csvFile = open(settings.SHEET_PATH, "r", encoding="utf-8")
        reader = csv.reader(csvFile)
        user_settings = {}
        # 迭代所有的行
        for row in reader:
            if "T" in row[0]:
                tool_num = row[0]
                s = row[1]
                f = row[2]
                model = row[3]
                val1 = row[4]
                val2 = row[5]
                user_settings[tool_num] = {
                    "feed": int(f),
                    "speed": int(s),
                    "model": model,
                    "var1": float(val1),
                    "var2": float(val2),
                }
        return user_settings

    def set_machineinfo_from_file(self):
        """
        获取并设定用户提供的机台刀具信息
        """
        self.user_settings = self.read_user_settings()

    def make_vibDate_cache(self):
        """
        把振动数据缓存起来

        """
        #print(self.机台正在加工())
        # 缓存健康度计算数据
        if self.机台正在加工():
            self.vibData_cache.append(self.pre_data)

        self.raw_vibData_cache.extend(self.pre_data)
    def 判断机台进给(self):
        if self.set_feed - 100 < self.act_feed and self.act_feed < self.set_feed + 100:
            return True
        return False
    def 判断机台转速(self):
        if self.set_speed - 100 < self.act_speed and self.set_speed < self.set_feed + 100:
            return True
        return False
    def 机台正在加工(self):
        if self.判断机台转速() and self.判断机台进给():
            return True
        return False

    @clothes(settings.RAWVIBDATA_UPLOAD_BLANKING_TIME)
    def 发送振动数据到云端(self):
        """
        降维原始振动数据
        发送降维后数据到云端
        清空本地缓存
        :return:
        """
        self.处理振动数据()
        self.put_vibdata_to_cloud(self.processed_raw_vibData)
        self.raw_vibData_cache = []
        
    def put_vibdata_to_cloud(self, data):
        """
        把处理过的振动数据 通过websocket发送到指定地址
        :param data:
        :return:
        """
        data = ",".join([str(i) for i in data])
        try:
            
            self.hub.server.invoke("broadcastDJJK_FZ", self.companyNo, self.deviceNo, self.now_str, data)
        except Exception as e:
            print(e)
            self.ready = False

    def 处理振动数据(self):
        """
        把振动数据降维处理
        :return:
        """
        self.processed_raw_vibData = self.raw_vibData_cache[:60]

    @clothes(settings.TOOLHEALTH_COMPUTE_BLANKING_TIME, True)
    def 处理健康度(self):
        """
        通过算法把缓存的振动数据处理成刀具健康度然后发送到指定端口
        :return:
        """
        H, flag_notch, flag_wear = self.运行对应算法计算健康度()
        self.tool_hp_pre = self.tool_hp
        self.tool_hp = H

        self.发送健康度到云端()
        self.刀具报警判断()
        self.发送健康度到API()
        self.clean_vibdata_cache()
    def 刀具报警判断(self):
        """
        根据刀具健康度与前一个计算的健康度差值进行报警处理
        :return:
        """
        # 如果前一个健康度小于后一个健康度则不判断
        if self.tool_hp_pre < self.tool_hp:
            return False
        hp_abs_val = self.tool_hp_pre - self.tool_hp
        alpha = self.user_settings[self.tool_num]["var1"]
        beta = self.user_settings[self.tool_num]["var2"]
        flag = 0
        if beta < hp_abs_val < alpha:
            flag = 1
            print("磨损报警")
        elif alpha <= hp_abs_val < 0.5:
            print("崩缺报警")
            flag = 2
        elif 0.5 <= hp_abs_val:
            print("断刀报警")
            flag = 3
        if self.load > 100:
            self.进行机台报警()
        if flag:
            self.进行机台报警()
            self.进行UI报警()

        pass
    def 健康度报警(self):
        self.进行UI报警()
        try:
            self.进行机台报警()
        except Exception as e:
            print(e)

    def 发送健康度到API(self):
        data = settings.TOOL_HP_CACHE_POST_PARRM
        data["collect_data"] = self.tool_hp
        data["start_date"] = self.now_str
        data["tool_position"] = self.tool_num
        resp = self.s.post(settings.TOOL_HP_CACHE_POST_URL, data=data)
        
    def 进行UI报警(self):
        print("ui报警")
        json_data = [
            {
                "machine_num": "1",
                "data": [
                    self.tool_num,
                ]

            },
        ]
        self.hub.server.invoke("BroadcastDJJK_Alarm", self.companyNo, json.dumps(json_data))
        

            
    def 进行机台报警(self):
        print("机台报警")
        os.add_dll_directory(r'D:\znmx_xc\znmx_xc-master1');
        so = ctypes.cdll.LoadLibrary
        lib = so(r'D:\znmx_xc\znmx_xc-master1\API.dll');
        #print(dir(lib))
        lib.setAlarm.restype = ctypes.c_char_p
        ret = lib.setAlarm(settings.MACHINE1_IP,len(settings.MACHINE1_IP),802, 3);
        
    def 进行报警(self):

        json_data = [
            {
                "machine_num": "1",
                "data": [
                    "T01",
                    "T02",
                    "T03",
                ]

            },
            {
                "machine_num": "2",
                "data": [
                    "T01",
                    "T02",
                    "T03",
                ]

            },
        ]
        self.hub.server.invoke("BroadcastDJJK_Alarm", self.companyNo, json.dumps(json_data))

    def 运行对应算法计算健康度(self):
        model = self.user_settings[self.tool_num]["model"]
        alpha = self.user_settings[self.tool_num]["var1"]
        beta = self.user_settings[self.tool_num]["var2"]
        try:
            ret = self.alarm(self.vibData_cache, float(alpha), float(beta))
        except Exception as e:
            print(e)
            ret = 0, False, False
        return ret


    '''
    输入：数据raw_data、崩缺调整系数alpha、磨损调整系数beta
    输出：健康度H、崩缺报警标志flag_notch、磨损报警标志flag_wear
    '''

    def alarm(raw_data, alpha=1, beta=5):
        flag_wear = 0
        flag_notch = 0
        data = []
        for i in range(len(raw_data)):
            data += raw_data[i]

        data = np.array(data)
        rms = sqrt(np.sum(np.int64((data * alpha) ** 2)) / len(data))

        # 崩缺报警
        if rms > 200:
            flag_notch = 1

        # 磨损报警
        H = 1 / (1 + log(rms, 10 ** beta))
        if H < 0.8:
            flag_wear = 1

        return H, flag_notch, flag_wear
    def 发送健康度到云端(self):
        self.put_hpdata_to_cloud(self.tool_hp)
        print("发送到云端:健康度->%s,刀具->%s"%(self.tool_hp, self.tool_num))

    def put_hpdata_to_cloud(self, data):
        companyNo = "CMP20210119001"
        deviceNo = '0001'
        try:
            self.hub.server.invoke("broadcastDJJK_Health", companyNo, deviceNo, self.tool_num, self.now_str, data*100)
        except Exception as e:
            print(e)
            self.ready = False

    def clean_vibdata_cache(self):
        self.vibData_cache = []

    @clothes(500)
    def show_info(self):
        """
        显示当前算法运行状况
        """

        print("当前机台->加工刀具:{2},当前转速/预设:{3}->{0},当前进给/预设:{4}->{1},负载:{5},当前健康度:{6},当前振动数据:{7},当前振动缓存数据{8},当前健康度缓存数据{9}, 机台是否转向"
              .format(self.set_speed, self.set_feed, self.tool_num,self.set_speed, self.set_feed, self.load, self.tool_hp, len(self.pre_data), len(self.raw_vibData_cache), len(self.vibData_cache)), self.机台正在加工())



    def run(self) -> None:
        """
        每1秒获取一次数据 每次10条 间隔100毫秒
        """
        while 1:
            self.setup()
            while self.ready:
                try:
                    self.prepare_machineInfo()
                    self.prepare_vibrationData()
                    if self.机台正在加工() and self.vibData_cache:
                        self.处理健康度()
                    self.发送振动数据到云端()
                    self.发送负载数据到云端()
                    self.show_info()

                except Exception as e:
                    print(e)
                    self.ready = False
            if not self.ready:
                print("五秒后重试")
                time.sleep(5)

if __name__ == '__main__':

    print("hello world")

    t = []

    t.append(ProcessData())
    for t1 in t:
        t1.start()
    for t1 in t:
        t1.join()