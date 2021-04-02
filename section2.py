"""
2021/1/22
created by wujiayun
生成不同比例的哨兵节点集合，并且存入文件
"""
import strategy as stg
import numpy as np
import init_net as init
import progressbar
import os
import time

# 参数
path_prefix = "G:\\sentinel\\sentinels data\\"  # 文件路径前缀
network_name = 'prostitution'  # 需要操作的网络名
view_period = 1  # 哨兵节点的观测期
sentinel_rate = 0.1  # 哨兵节点的比例
repeat_time = 100  # 重复的次数
name_list = ['random', 'acquaintances', 'most_active', 'weighted_most_active', 'recent', 'mid_link']

begin = time.time()
tn = init.init("G:\\sentinel\\networks\\prostitution\\prostitution1.csv")
progress = 0
result = []
with progressbar.ProgressBar(max_value=repeat_time) as bar:
    for i in range(repeat_time):
        r = stg.get_sentinels(tn, view_period, sentinel_rate)
        result.append(r)
        progress += 1
        bar.update(progress)
# 存文件
path = path_prefix + tn.graph['networks_name'] + '\\'
if not os.path.exists(path):
    os.mkdir(path)
file_name = 'view' + str(view_period) + 'rate' + str(sentinel_rate)
file_path = path + file_name
result = np.array(result)
np.save(file_path, result)
end = time.time()
print('write sentinels done time: ' + str(int(end - begin)) + 's')
