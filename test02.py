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
from ctypes import *

os.add_dll_directory('D:\Debug');
dll = cdll.LoadLibrary(r'D:\Debug\api.dll');
ret = dll.setAlarm(settings.MACHINE1_IP,len(settings.MACHINE1_IP),802, 3);
print(ret)