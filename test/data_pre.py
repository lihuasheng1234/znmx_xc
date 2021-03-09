import numpy as np
from math import *

'''
输入：数据raw_data、崩缺调整系数alpha、磨损调整系数beta
输出：健康度H、崩缺报警标志flag_notch、磨损报警标志flag_wear
'''
def alarm(raw_data, beta=0.75):
    flag_wear = 0
    data = []
    for i in range(len(raw_data)):
        data += raw_data[i]

    data = np.array(data)
    rms = sqrt(np.sum(np.int64((data) ** 2)) / len(data))

    # 磨损报警
    H = 1 / (1 + log(rms, 10 ** 4)) + 0.2
    if H < beta:
        flag_wear = 1

    return H, flag_wear
if __name__ == '__main__':
    print(alarm([[-1], []]))