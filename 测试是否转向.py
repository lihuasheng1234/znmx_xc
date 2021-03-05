import csv
import sqlite3

import settings


def read_user_settings():
    """
    通过本地表格文件读取用户设定
    :return:
    """
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
                "feed": f,
                "rspeed": s,
                "model": model,
                "var1": val1,
                "var2": val2,
            }
    return user_settings

def get_machineInfo():
    con = sqlite3.connect(settings.MACHINEINFO_DB_PATH)
    cur = con.cursor()
    print("Opened database successfully")

    cur.execute(settings.SQLITE_SQL)
    ret = cur.fetchone()
    print(ret)
    return {
        "load": ret[0],
        "feed": ret[2],
        "speed": ret[3],
        "tool_num": ret[4],

    }

def 判断刀具是否转向(machine_info, user_settings):
    now_s = machine_info['speed']
    now_f = machine_info['feed']

    set_s = user_settings['rspeed']
    set_f = user_settings['feed']

    if now_s == set_s and now_f == set_f:
        print("正在加工")
        return True
if __name__ == '__main__':
    user_settings = read_user_settings()
    machine_info = get_machineInfo()
    判断刀具是否转向(machine_info, user_settings)
