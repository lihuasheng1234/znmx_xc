import os
import json
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_PATH, "config.json")
with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
    #print(list(f.readlines()))
    json_data = json.load(f)
TOTAL_SETTINGS = json_data

# 时间字符串格式
DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"
# 训练数据保存格式
SAVEDDATA_FILENAME_FORMAT = "%Y-%m-%d-%H-%M-%S-%f"

# 负载报警阈值
MAX_LOAD_WARMING = 100

#是否为本地模式
IS_LOCAL = False

# 保存数据开关
LEARNNING_MODEL = False

# 计算健康度时间间隔 毫秒
TOOLHEALTH_COMPUTE_BLANKING_TIME = 3*1000

# 负载上传时间 毫秒
LOADDATA_UPLOAD_BLANKING_TIME = 1*1000

# 原始振动数据上传时间 毫秒
RAWVIBDATA_UPLOAD_BLANKING_TIME = 1*1000

# 数据库中振动数据每条数据间隔 毫秒
VIBDATA_DB_TIME = 100

# 每隔多少时间间隔获取一次机台信息 毫秒
LOADDATA_DB_GET_BLANKING_TIME = 100

# 从数据库获取振动数据间隔 毫秒
VIBDATA_DB_GET_BLANKING_TIME = 100

# 每个间隔内从数据库中获取的数据条数
VIBDATA_COUNT = VIBDATA_DB_GET_BLANKING_TIME//VIBDATA_DB_TIME

# 从数据库获取振动数据间隔 毫秒
LEARNNING_MODEL_BLANKING_TIME = 2*1000

#mangodb settings
vibdata_mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "VibrationData",
    "tb_name" : "Sensor03",
    "connect_timeoutMS" : "10000",
}

machineInfo_mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "FanucData",
    "tb_name" : "Machine01",
    "connect_timeoutMS" : "10000",
}

#websocket 发送配置
signalr_hub_info = {
    "url": TOTAL_SETTINGS["damage"]["signalr_url"] if not IS_LOCAL else "http://localhost:8070/signalr/",
    "name": TOTAL_SETTINGS["damage"]["signalr_hubname"],
}

# 读取用户设定文件配置

SHEET_PATH = os.path.join(BASE_PATH, "sheets.csv")


# 刀具健康度缓存数据接口
TOOL_HP_CACHE_POST_URL = TOTAL_SETTINGS["damage"]["data_post_params"] if not IS_LOCAL else "http://localhost:8054/api/TblDeviceFanuc/InsertToolDetect"
TOOL_HP_CACHE_POST_PARRM = {
        "company_no": "CMP20210119001",
        "device_no": "0001",
        "tool_position": "",
        "collect_data": "",
        "collect_date": "2021-02-24 14:13:00"
    }

MACHINE1_IP = "192.168.1.1"

MACHINEINFO_DB_PATH = r'C:\Users\57852\Desktop\fanuc_iot.db'
SQLITE_SQL = "select SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM, ACT_FEED, ACT_SPEED from FANUC_IOT order by ID desc limit 1;"

# 报警接口dll文件路径
DLL_PATH = BASE_PATH
DLL_NAME = os.path.join(DLL_PATH, "API.dll")

# 日志配置参数
kwargs = {
    "filename": "logs.txt",
    "format": "%(asctime)s - %(message)s",
    "mode": "a",
}

company_no = TOTAL_SETTINGS["company_no"]
device_no = TOTAL_SETTINGS["device_no"]

WORKING_HUB_NAME = TOTAL_SETTINGS["damage"]["raw_send_funcname"]
FZ_HUB_NAME = TOTAL_SETTINGS["damage"]["load_send_funcname"]
HEALTH_HUB_NAME = TOTAL_SETTINGS["damage"]["rws_send_funcname"]
ALARM_HUB_NAME = TOTAL_SETTINGS["damage"]["alarm_send_funcname"]
