import pymysql

# 时间字符串格式
DATETIME_PATTERN = "%Y-%m-%d-%H-%M-%S"

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

# 刀具健康度mysql
hp_mysql_info = {
    "host" : "192.168.1.33",  # mysql服务端ip
    "port" : 3306,  # mysql端口
    "user" : "root",  # mysql 账号
    "password" : "root",
    "db" : "znmx",
    "charset" : "utf8",
    "cursorclass" : pymysql.cursors.DictCursor
}

#mangodb settings
mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "VibrationData",
    "tb_name" : "Sensor03",
    "connect_timeoutMS" : "10000",
}

signalr_hub_info = {
    "url": "http://202.104.118.59:8070/signalr/",
    "name": "dashBoardHub",
}

# 读取用户设定文件配置
SHEET_PATH = "sheets.xlsx"

# 刀具健康度缓存数据接口
TOOL_HP_CACHE_POST_URL = "http://202.104.118.59:8054/api/TblDeviceFanuc/InsertToolDetect"
TOOL_HP_CACHE_POST_PARRM = {
        "company_no": "CMP20210119001",
        "device_no": "0001",
        "tool_position": "",
        "collect_data": "",
        "collect_date": "2021-02-24 14:13:00"
    }

MACHINE1_IP = "111.111.1.1"
MACHINE2_IP = "111.111.1.1"