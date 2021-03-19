# import os
# import ctypes
import settings
# print(settings.BASE_PATH)
#
# os.add_dll_directory(r"C:\Users\57852\Desktop\test01\znmx_xc")
# so = ctypes.cdll.LoadLibrary
# dll_path = os.path.join(settings.BASE_PATH, "API.dll")
# lib = so("api.dll")
# lib.setAlarm.restype = ctypes.c_char_p
# ret = lib.setAlarm(settings.MACHINE1_IP,len(settings.MACHINE1_IP),802, 3);
# print(ret)
# input()
import os
import sys
import ctypes
import settings
def activate_alarm(machine_ip, alarm_flag, alarm_No):
    base_path = settings.BASE_PATH
    # !! Necessary for Python to Change Current Working Directory before loading dll
    os.chdir(os.path.join(base_path, 'Alarm_API'))
    lib = ctypes.cdll.LoadLibrary('API.dll')
    lib.setAlarm.restype = ctypes.c_int
    ret = lib.setAlarm(machine_ip, len(machine_ip), alarm_flag, alarm_No)
    os.chdir(base_path)
   

if __name__ == "__main__":
    machine_ip = "192.168.1.1"  # 设备IP地址
    activate_alarm(machine_ip, 511, 3)
    
   