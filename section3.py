"""
2021/1/22
created by wujiayun
读取感染过程文件，对策略进行评估
"""
import os
import matplotlib.pyplot as plt
import progressbar
import time
import numpy as np

# 固定参数
simulation_dir = "G:\\sentinel\\simulation data\\"
sentinels_dir = "G:\\sentinel\\sentinels data\\"

# 可选参数
network_name = 'prostitution'
beta = 0.9
niu = 100000.0
period = 0.75
rate = 0.1

simulation_file = simulation_dir + network_name + '\\beta' + str(beta) + 'niu' + str(niu) + '.npy'
simulation = np.load(simulation_file, allow_pickle=True)
sentinels_file = sentinels_dir + network_name + '\\view' + str(period) + 'rate' + str(rate) + '.npy'
sentinels = np.load(sentinels_file, allow_pickle=True)
avg_response_distance = np.zeros(6)  # 记录初次响应的距离
avg_sentinels_inf_size = np.zeros(6)  # 记录哨兵节点集合的平均感染大小
break_size = []  # 记录每个感染过程的感染规模
progress = 0
counter = 0
begin = time.perf_counter()
with progressbar.ProgressBar(max_value=len(simulation)) as bar:
    for sir in simulation:  # 一次sir仿真过程
        break_size.append(len(sir))
        if not len(sir) == 1:  # 具有感染规模的情况下
            for i in np.arange(1, len(sir), 1):  # 一次仿真过程中的一个感染节点信息集
                sentinels_counter = np.zeros(6)
                for sen in sentinels:  # 一组哨兵节点集合
                    for j in range(6):  # 一种哨兵节点集合中的一个哨兵节点
                        if sir[i][0] in sen[j]:  # s 是集合查询效率比list高
                            if sentinels_counter[j] == 0 and i < len(sir) - 1:
                                avg_response_distance[j] += i / len(sir)
                                counter += 1
                            sentinels_counter[j] += 1  # 统计总的哨兵节点所占的比例
                sentinels_counter = sentinels_counter / 100
                avg_sentinels_inf_size += sentinels_counter
        progress += 1
        bar.update(progress)
break_size = np.array(break_size)
avg_response_distance = avg_response_distance / (break_size.mean() - 1)  # 消除不同爆发规模带来的影响
avg_response_distance = avg_response_distance / 10  # 划为%制
break_size.sort()
# 绘制感染规模的直方统计图 begin
plt.figure(dpi=300)  # 设置分辨率为300
fig = plt.hist(break_size, bins=20, facecolor="tomato", edgecolor="c", alpha=0.7)  # 用偏红的颜色代替感染规模
plt.title(network_name + '\nβ:' + str(beta) + ' μ:' + str(1 / niu))
plt.axvline(break_size.mean(), color='y', ls=':')
plt.text(break_size.mean(), 100, str(break_size.mean()), ha='left')
plt.xlabel('Outbreak size')
path = "G:\\sentinel\\images\\" + network_name + "\\break_size\\"
if not os.path.exists(path):
    os.makedirs(path)  # 创建多层文件夹 单层可用mkdir
plt.savefig(path + 'β' + str(beta) + 'μ' + str(1 / niu) + '.png')
plt.show()
plt.close()
# 绘制感染规模的直方统计图 end
print(avg_response_distance)
print(avg_sentinels_inf_size)
print(break_size.mean())
end = time.perf_counter()
