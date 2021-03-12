import settings
import json

with open(settings.SETTINGS_PATH, 'r', encoding='utf-8') as f:
    #print(list(f.readlines()))
    json_data = json.load(f)
print(json_data["damage"])


def read_user_settings():
    """
    通过本地表格文件读取用户设定,
    读取出来的数据均为字符串
    :return:
    """
    user_settings = {}
    # 迭代所有的行
    for key in settings.json_data["damage"]:
        if key.startswith("T"):
            temp = settings.json_data["damage"][key].split(',')
            tool_num = key
            s = 0
            f = 0
            model = temp[0]
            val1 = temp[1]
            val2 = temp[2]
            user_settings[tool_num] = {
                "feed": float(f),
                "speed": float(s),
                "model": model,
                "var1": float(val1),
                "var2": float(val2),
            }
    return user_settings
print(read_user_settings())