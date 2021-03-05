import sqlite3
def get_machineInfo():
    con = sqlite3.connect(r'D:\fanuc\debug\fanuc_iot.db')
    cur = con.cursor()
    print("Opened database successfully")

    cur.execute("select SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM from FANUC_IOT order by ID desc limit 1;")
    ret = cur.fetchone()
    print(ret)
    return {
        "load": ret[0],
        "feed": ret[2],
        "speed": ret[3],
        "tool_num": ret[4],

        }