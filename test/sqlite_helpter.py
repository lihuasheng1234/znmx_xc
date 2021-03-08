import sqlite3

con = sqlite3.connect(r'D:\fanuc\debug\fanuc_iot.db')
cur = con.cursor()
print("Opened database successfully")

cur.execute("select SPINDLE_LOAD, SET_FEED, SET_SPEED, TOOL_NUM,DATE from FANUC_IOT order by ID desc limit 1;")
print(cur.fetchone())