import sqlite3
def get_machineInfo():
    con = sqlite3.connect(r'C:\Users\57852\Desktop\fanuc_iot.db')
    cur = con.cursor()
    #print("Opened database successfully")

    cur.execute("select SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM from FANUC_IOT order by ID desc limit 1;")
    ret = cur.fetchone()
    print(ret)
    return {
        "load": ret[0],
        "feed": ret[1],
        "speed": ret[2],
        "tool_num": ret[3],

        }
if __name__ == '__main__':
    get_machineInfo()