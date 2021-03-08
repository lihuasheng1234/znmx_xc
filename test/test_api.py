import requests
import settings


times = 5
start_date = '2021-02-24 14:13:00'
test_data = ""
test_data = test_data.split(",")
test_data = test_data*times

url = "http://202.104.118.59:8054/api/TblDeviceFanuc/InsertToolDetect"
s = requests.Session()

data = settings.TOOL_HP_CACHE_POST_PARRM
data["collect_data"] = ",".join(test_data)
data["start_date"] = start_date
data["tool_position"] = "T01"
print(data)

resp = s.post(settings.TOOL_HP_CACHE_POST_URL, data=data)

print(resp.text)
print(resp.request.headers)
print(resp.headers)