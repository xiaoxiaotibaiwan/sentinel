"""
读取仿真结果与哨兵节点集合，计算指标DL DT PA
"""

import progressbar
import numpy as np

# 固定参数
simulation_dir = "G:\\sentinel\\simulation data\\"
sentinels_dir = "G:\\sentinel\\sentinels data\\prostitution\\"


# 可选参数
def analyse(network_name, beta, niu, net, sentinels, windows):
    simulation_file = simulation_dir + network_name +  '\\beta' + str(beta) + 'niu' + str(niu) + '.npy'
    simulation = np.load(simulation_file, allow_pickle=True)
    detected_time = []
    detected_public = []
    sentinels_size = len(sentinels)
    break_size = []  # 记录每个感染过程的感染规模
    progress = 0
    count = 0
    with progressbar.ProgressBar(max_value=len(simulation)) as bar:
        for sir in simulation:  # 一次sir仿真过程
            break_size.append(len(sir))
            if len(sir) > 1:  # 未感染的就不管
                count += 1
                flag = False  # 标志位
                for i in np.arange(1, len(sir), 1):  # 一次仿真过程中的一个感染节点信息集
                    for j in range(sentinels_size):  # 一组哨兵节点集合中的一个哨兵节点
                        if flag:
                            break
                        if sir[i][0] in sentinels:  # 检测到的情况
                            time = (sir[i][1] - sir[0][1]) / windows
                            public = i / (len(sir) - 1)
                            detected_time.append(time)
                            detected_public.append(public)
                            flag = True
            progress += 1
            bar.update(progress)
    DL = len(detected_time) / count  # 只记录具有爆发规模的情况
    DT = np.mean(detected_time)
    PA = np.mean(detected_public)
    # break_size = np.mean(break_size)   # 顺便统计一下平均爆发规模
    return DL, DT, PA


# sentinels = np.load("G:\\sentinel\\sentinels data\\prostitution\\ws1-6-lambda=1.npy", allow_pickle=True)
sentinels = np.loadtxt("G:\\sentinel\\sentinels data\\prostitution\\d(4-6).csv", dtype='int')
p = 1
result = []
result.append(analyse('prostitution4-6', 0.5, 0.5, p+2, sentinels[:100], 372))
# for p in range(2, 5, 1):
#     result.append(analyse('prostitution', 1, 1, p+2, sentinels[p][:300], 372))
save_path = "G:\\sentinel\\results\\prostitution\\d(4-6)-100.csv"
np.savetxt(save_path, result, fmt='%.5f')
