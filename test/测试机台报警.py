import ctypes
import os

import settings

machine_ip = settings.MACHINE1_IP
alarm_flag = 511
alarm_No = 3
base_path = settings.BASE_PATH
os.chdir(os.path.join(base_path, 'Alarm_API'))
lib = ctypes.cdll.LoadLibrary('API.dll')
lib.setAlarm.restype = ctypes.c_int
ret = lib.setAlarm(machine_ip, len(machine_ip), alarm_flag, alarm_No)
os.chdir(base_path)