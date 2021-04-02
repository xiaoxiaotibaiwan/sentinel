# 基于peter Holmes 的时序网络上的快速SIR算法
# 核心还是用空间来换时间

from copy import deepcopy
import random
import networkx as nx
import numpy as np


class Heap:
    """
    二叉优先排序堆

  定义所需的小根堆，按时间戳关键字确定优先，保证模型传播符合时间先后顺序
  包含插入:insert, 删除:delete操作
  堆的第一放为1，方便二叉树的操作
 （节点：node, 感染时间： inf_time）
    """

    heap = [1]
    infected_nodes = []  # 记录感染节点序列

    # 堆的插入操作
    def insert(self, event):
        self.heap.append(event)
        child = len(self.heap) - 1
        while child > 0:
            parent = child // 2
            if parent > 0 and self.heap[parent][1] > self.heap[child][1]:
                self.heap[parent], self.heap[child] = self.heap[child], self.heap[parent]
            child = parent

    # 堆的删除操作
    def delete(self):
        # 交换
        self.heap[1], self.heap[-1] = self.heap[-1], self.heap[1]
        # 删除最后一个
        del self.heap[-1]
        parent = 1
        while parent < len(self.heap):
            l_child = 2 * parent
            r_child = l_child + 1
            min_child = l_child
            if r_child < len(self.heap):  # 存在两个孩子的情况
                if self.heap[l_child][1] > self.heap[r_child][1]:
                    min_child = r_child
            if l_child < len(self.heap) and self.heap[min_child][1] < self.heap[parent][1]:  # 交换
                self.heap[parent], self.heap[min_child] = self.heap[min_child], self.heap[parent]
                parent = min_child
            else:
                break


def contagious_contact(time_stamp_list, now, beta):
    """
用来查找是否有联系和返回拟定感染的时间戳，其中查找使用二分查找。
正常返回拟定感染时间，无匹配结果返回 -1
    :type time_stamp_list: list
    :param time_stamp_list: 时间戳列表
    :param now: 当前时间戳
    :param beta: 感染率
    :return: 欲感染的时间戳位置
    """
    low = 0
    mid = 0
    hi = len(time_stamp_list) - 1

    if time_stamp_list[-1] <= now:
        return -1
    # 利用二分查找，找到第一个大于now的时间戳
    while low < hi:
        mid = (low + hi) // 2
        if time_stamp_list[mid] > now:
            hi = mid
        else:
            low = mid + 1
    # (int((math.log(1 - random.random())) / (math.log(1 - beta))))
    hi = hi + np.random.geometric(beta) - 1  # 采样生成感染的时间
    if hi >= len(time_stamp_list):  # 超过了最大时间线
        return -1
    return time_stamp_list[hi]


def after_infected(h, infected_node, duration):
    """
当节点被感染后所需要进行的操作，统计，变量赋值等等
    :param duration: 持续时间
    :param h: 二叉优先排序堆
    :param infected_node: 感染节点信息

    """
    h.infected_nodes.append((infected_node[0], infected_node[1], duration))


def infect(g, h, node_list, beta, nu):
    """
单个感染进程，给定感染节点，节点感染时间，节点恢复时间，感染其邻居节点
    :type g: nx.Graph
    :param g: 时序网络
    :param h: 堆
    :param node_list: 存放节点状态信息的字典
    :param beta: 感染率
    :param nu: 恢复率
    """
    infected_node = h.heap[1]
    h.delete()
    if node_list[infected_node[0]]['state'] == 'infected':  # 说明该节点在此之前已经被感染
        return
    duration = int(np.random.exponential(nu))
    after_infected(h, infected_node, duration)
    node_list[infected_node[0]]['state'] = 'infected'
    if duration > 0:  # 如果持续时间小于0，那么疫情将无法传播
        deadline = infected_node[1] + duration
        for nbr in g[infected_node[0]]:
            if node_list[nbr]['state'] != 'infected':
                t = contagious_contact(list(g.edges[infected_node[0], nbr]['time_stamp']), infected_node[1], beta)
                if t != -1 and t <= deadline:
                    h.insert([nbr, t])


def sir(g, beta, nu):
    """
    :param g: 时序网络
    :param rate: 观测期划分 /未启用
    :param beta:感染率
    :param nu:恢复率
    :type g: nx.Graph
    """
    # -------------------初始化---------------------
    # nu = int(g.graph['time_stamp_list'][-1] * nu)
    nu = int(nu*372)
    h = Heap()
    h.infected_nodes = []
    time_windows = g.graph['time_stamp_list'][-1]  # 总的时间戳长度，实际时间
    seed = random.randint(0, len(g) - 1)
    # 防止数据污染，表示状态的属性每次模型都应该是单独的内存
    node_list = deepcopy(g.nodes)
    seed_node = list(node_list)[seed]
    inf_time = random.randint(g.graph['time_stamp_list'][0], g.graph['time_stamp_list'][-1])
    h.insert([seed_node, inf_time])
    # -----------------初始化完毕----------------------
    while len(h.heap) > 1:
        infect(g, h, node_list, beta, nu)
    del node_list
    return h.infected_nodes


# G = init_net.init('G:\\sentinel\\networks\\messages.csv')
# init_net.network_analyze_basic(G)
# avg = 0
# count = 0
# re = []
# with progressbar.ProgressBar(max_value=1000) as bar:
#     for i in range(1000):
#         r = sir(G, 1, 1, 1)
#         re.append(r)
#         avg += len(r)
#         count += 1
#         bar.update(count)
# print(avg)