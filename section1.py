"""
2021/1/20
created by wujiayun
用于跑SIR模型，并且把跑的结果保存为csv文件

"""
import init_net as init
import SIRModel as model
import time
import numpy as np
import progressbar
import os

# --变量--
network_path = 'G:\\sentinel\\networks\\prostitution\\prostitution4-6.csv'  # 拟读取网络的地址
infection_rate = 0.5  # 感染率[0, 1) 取1的情况会有概率出现除0报错
recover_rate = 0.5  # 恢复率(0, infinite) 这里为了方便起见 直接取得倒数，也就是期望值
repeat_time = 10000  # 重复次数
# --变量--

begin = time.perf_counter()  # py3.8
tn = init.init(network_path)
simulation_result = []
progress = 0

# SIR MODEL
with progressbar.ProgressBar(max_value=repeat_time) as bar:
    for i in range(repeat_time):
        r = model.sir(tn, infection_rate, recover_rate)
        simulation_result.append(r)
        progress += 1
        bar.update(progress)

# FILE SAVE
path = "G:\\sentinel\\simulation data\\" + tn.graph['networks_name']
if not os.path.exists(path):
    os.mkdir(path)
file_name = 'beta' + str(infection_rate) + 'niu' + str(recover_rate)
file_path = path + '\\' + file_name
describe_list = [tn.graph['networks_name'], 'beta:' + str(infection_rate), 'niu:' + str(recover_rate), 'repeat_time:' +
                 str(repeat_time)]
simulation_result = np.array(simulation_result, dtype="object")
np.save(file_path, simulation_result)   # 持久化
end = time.perf_counter()
print('sir模型运行完毕 用时：' + str(int(end - begin)) + '秒')
