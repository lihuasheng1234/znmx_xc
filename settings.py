import pymysql

# 时间字符串格式
DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"

# 负载小于到少判断为主轴未转动
MIN_VALUE = 0

#mysql settings
mysql_info = {
    "host" : "192.168.1.33",  # mysql服务端ip
    "port" : 3306,  # mysql端口
    "user" : "root",  # mysql 账号
    "password" : "root",
    "db" : "znmx",
    "charset" : "utf8",
    "cursorclass" : pymysql.cursors.DictCursor
}

IS_LOCAL = False

# 计算健康度时间间隔 毫秒
TOOLHEALTH_COMPUTE_BLANKING_TIME = 5*1000

# 负载上传时间 毫秒
LOADDATA_UPLOAD_BLANKING_TIME = 1*1000

# 原始振动数据上传时间 毫秒
RAWVIBDATA_UPLOAD_BLANKING_TIME = 1*1000

# 数据库中振动数据每条数据间隔 毫秒
VIBDATA_DB_TIME = 100

# 每隔多少时间间隔获取一次机台信息 毫秒
LOADDATA_DB_GET_BLANKING_TIME = 250

# 从数据库获取振动数据间隔 毫秒
VIBDATA_DB_GET_BLANKING_TIME = 100

# 每个间隔内从数据库中获取的数据条数
VIBDATA_COUNT = VIBDATA_DB_GET_BLANKING_TIME//VIBDATA_DB_TIME


#mangodb settings
mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "VibrationData",
    "tb_name" : "Sensor03",
    "connect_timeoutMS" : "10000",
}

hub_url = "http://202.104.118.59:8070/signalr/" if not IS_LOCAL else "http://localhost:8070/signalr/"
signalr_hub_info = {
    "url": hub_url,
    "name": "dashBoardHub",
}

# 读取用户设定文件配置
SHEET_PATH = r"D:\znmx_xc\test01\znmx_xc-master\sheets.csv"

# 刀具健康度缓存数据接口
TOOL_HP_CACHE_POST_URL = "http://202.104.118.59:8054/api/TblDeviceFanuc/InsertToolDetect" if not IS_LOCAL else "http://localhost:8054/api/TblDeviceFanuc/InsertToolDetect"
TOOL_HP_CACHE_POST_PARRM = {
        "company_no": "CMP20210119001",
        "device_no": "0001",
        "tool_position": "",
        "collect_data": "",
        "collect_date": ""
    }

MACHINE1_IP = "10.143.60.119"


MACHINEINFO_DB_PATH = r'D:\fanuc\debug\fanuc_iot.db'
SQLITE_SQL = "select SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM from FANUC_IOT order by ID desc limit 1;"

DLL_PATH = r'D:\znmx_xc\znmx_xc-master\Debug'
DLL_NAME = r'D:\znmx_xc\znmx_xc-master\Debug\API.dll'