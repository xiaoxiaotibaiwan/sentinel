"""
生成哨兵节点集合
"""
import strategy as stg
import init_net as init
import numpy as np


def get_ws():
    data = []
    for i in range(1, 7, 1):
        G = init.init("G:\\sentinel\\networks\\prostitution\\prostitution" + str(i) + ".csv")
        w_s = stg.weighted_strength(G, 372, i, 1)
        t = np.array(w_s, dtype='int')
        t = t[:500, 0]  # 保留前500位
        data.append(t)
    np.save('G:\\sentinel\\sentinels data\\prostitution\\lambda=1', data)


def get_degree():
    data = []
    # for i in range(1, 7, 1):
    G = init.init("G:\\sentinel\\networks\\prostitution\\prostitution4-6.csv")
    w_s = stg.degree(G)
    t = np.array(w_s, dtype='int')
    t = t[:500, 0]  # 保留前500位
    data.append(t)
    np.savetxt('G:\\sentinel\\sentinels data\\prostitution\\d(4-6).csv', data, fmt='%d')


def get_strength():
    data = []
    # for i in range(1, 7, 1):
    G = init.init("G:\\sentinel\\networks\\prostitution\\prostitution4-6.csv")
    w_s = stg.strength(G)
    t = np.array(w_s, dtype='int')
    t = t[:500, 0]  # 保留前500位
    data.append(t)
    np.savetxt('G:\\sentinel\\sentinels data\\prostitution\\s(4-6).csv', data, fmt='%d')


get_degree()
get_strength()