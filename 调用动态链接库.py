import os
from ctypes import *
import settings

os.add_dll_directory(r'D:\znmx_xc\znmx_xc-master\Debug');
dll = cdll.LoadLibrary(r'D:\znmx_xc\znmx_xc-master\Debug\API.dll');

ret = dll.setAlarm("10.143.60.119", 1);
print(ret)