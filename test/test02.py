import os
import ctypes
import settings
print(settings.BASE_PATH)

os.add_dll_directory(settings.BASE_PATH)
so = ctypes.cdll.LoadLibrary
dll_path = os.path.join(settings.BASE_PATH, "API.dll")
lib = so(dll_path)
#print(dir(lib))
lib.setAlarm.restype = ctypes.c_char_p
ret = lib.setAlarm(settings.MACHINE1_IP,len(settings.MACHINE1_IP),802, 3);
print(ret)
input()