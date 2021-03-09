import os, sys
import ctypes
import settings

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)
os.add_dll_directory(BASE_PATH);
so = ctypes.cdll.LoadLibrary
lib = so(r'D:\znmx_xc\znmx_xc-master1\API.dll');
#print(dir(lib))
lib.setAlarm.restype = ctypes.c_char_p
ret = lib.setAlarm(settings.MACHINE1_IP,len(settings.MACHINE1_IP),802, 3);
print(ret)
input()