import csv
import settings
csvFile = open(r"sheets.csv", "r", encoding="utf-8")
reader = csv.reader(csvFile)

# 建立空字典
result = {}
for item in reader:
    # 忽略第一行

    if "T" in item[0]:
        print(item)
csvFile.close()


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
print(read_user_settings())