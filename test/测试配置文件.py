import sys

import settings
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(r'C:\Users\57852\Desktop\test01\znmx_xc\config.ini', encoding="utf-8")
cfg.set('installation','prefix', settings.BASE_PATH)
cfg.set('installation','test1', "崩缺调整系数α")
with open (r'C:\Users\57852\Desktop\test01\znmx_xc\config.ini', 'w+', encoding="utf-8") as f:
    cfg.write(f)

print(cfg.sections())
print(cfg.get('installation','prefix'))
