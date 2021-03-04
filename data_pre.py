import numpy as np
from math import *

'''
输入：数据raw_data、崩缺调整系数alpha、磨损调整系数beta
输出：健康度H、崩缺报警标志flag_notch、磨损报警标志flag_wear
'''
def alarm(raw_data, alpha=1, beta=5):
    flag_wear = 0
    flag_notch = 0
    data = []
    for i in range(len(raw_data)):
        data += raw_data[i]

    data = np.array(data)
    rms = sqrt(np.sum(data ** 2) / len(data))

    # 崩缺报警
    H2 = rms / (alpha + rms)
    if H2 < 0.2:
        flag_notch = 1

    # 磨损报警
    H = 1 / (1 + log(rms, 10 ** beta))
    if H < 0.8:
        flag_wear = 1

    return H, flag_notch, flag_wear