from signalr import Connection
from requests import Session

with Session() as session:
    #create a connection
    connection = Connection("http://202.104.118.59:8070/signalr/", session)

    #get chat hub
    hub = connection.register_hub('dashBoardHub')
    #start a connection
    connection.start()
    #create error handler
    def print_error(error):
        print('error: ', error)
        # process errors
    connection.error += print_error
    companyNo = "CMP20210119001"
    deviceNo = '0001'
    data = "10, 10, 10"
    data_raw = "200, 7, 200"
    import time, json
    json_data = [
        {
            "machine_num": "1",
            "data":[
                "T01",
                "T02",
                "T03",
                ]
            
        },
        {
            "machine_num": "2",
            "data":[
                "T01",
                "T02",
                "T03",
                ]
            
        },
    ]
    print(json.dumps(json_data))
    hub.server.invoke("BroadcastDJJK_Alarm", companyNo, json.dumps(json_data))
    i = 0
    #hub.server.invoke("broadcastDJJK_Health", companyNo, deviceNo, "T01", "2021-01-26 08:38:00", "1")
    while True:

        if i < 10:
            time1 = "2021-01-26 08:38:0" + str(i)
        else:
            time1 = "2021-01-26 08:38:" + str(i)
        hub.server.invoke("broadcastDJJK_Working", companyNo, deviceNo, time1, data_raw)
        hub.server.invoke("broadcastDJJK_FZ", companyNo, deviceNo, time1, data)
        #if i == 59:
        hub.server.invoke("broadcastDJJK_Health", companyNo, deviceNo, "T02", time1, "0.5")
        i += 1
        i = i % 60
        time.sleep(1)
        print(i)