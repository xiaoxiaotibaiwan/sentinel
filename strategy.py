# 所有的哨兵策略
import random
import math
import numpy as np


def binary_search(time_stamp_list, aim_value):  # [二分查找] 返回不超过目标值的最大时间戳的位置 (time_stamp_list: 有序时间戳数组, aim_value:目标值)
    low = 0
    high = len(time_stamp_list) - 1
    mid = 0
    while low <= high:
        mid = (low + high) // 2
        if time_stamp_list[mid] == aim_value:
            return mid
        else:
            if time_stamp_list[mid] > aim_value:
                high = mid - 1
            else:
                low = mid + 1
    if high < 0:
        return -1
    else:
        return mid


# [随机选择策略] 所有策略都采用该策略产生的随机节点列表
def random_select(G, rate):
    sentinel_num = int(len(G) * rate)
    nodes = list(G.nodes)  # 所有节点列表
    random_sentinels = random.sample(range(0, len(G.nodes)), sentinel_num)  # 随机采样方法
    sentinels = []  # 存储选定的哨兵节点
    for item in random_sentinels:
        sentinels.append(nodes[item])
    return sentinels


# [熟人策略]
def acquaintances(G, random_list):
    count = 0
    acquaintance = []
    for node in random_list:
        aim_node = -1
        if len(G[node]) > 0:
            aim_node = list(G[node])[random.randint(0, len(G[node]) - 1)]  # 随机选择一个邻居
        if aim_node not in random_list and aim_node != -1:  # 查询是否重复
            acquaintance.append(aim_node)
        else:
            acquaintance.append(node)
            count = count + 1  # 记录出现公共节点的次数
    sentinels = [acquaintance, count]
    return sentinels


# [最活跃策略]
def most_active(G, random_list, start_time):
    count = 0
    active = []
    for node in random_list:
        max_link = 0
        aim_node = -1
        for neighbour in G[node]:
            time = binary_search(G[node][neighbour]['time_stamp'], start_time) + 1
            if max_link < time:
                max_link = time
                aim_node = neighbour
        if aim_node not in random_list and aim_node != -1:  # 查询是否重复
            active.append(aim_node)
        else:
            active.append(node)
            count = count + 1  # 记录出现公共节点的次数
    sentinels = [active, count]
    return sentinels


# [带权最活跃策略] 越近的时间戳权重越高
def weighted_most_active(G, random_list, start_time, weight):
    count = 0
    weighted = []
    for node in random_list:
        weighted_max_link = 0
        aim_node = -1
        for neighbour in G[node]:
            position = binary_search(G[node][neighbour]['time_stamp'], start_time)
            temp = 0
            if position != -1:
                for snapshot in G[node][neighbour]['time_stamp'][:position]:
                    temp = temp + math.pow(weight, start_time - snapshot)  # 按照幂来分配权重
                if weighted_max_link < temp:
                    weighted_max_link = temp
                    aim_node = neighbour
        if aim_node not in random_list and aim_node != -1:  # 查询是否重复
            weighted.append(aim_node)
        else:
            weighted.append(node)
            count = count + 1  # 记录出现公共节点的次数
    sentinels = [weighted, count]
    return sentinels


# [最近联系策略]  选择最后一个产生联系的边
def recent(G, random_list, start_time):
    count = 0
    re = []
    for node in random_list:
        most_recent = 0
        aim_node = -1
        for neighbour in G[node]:
            position = binary_search(G[node][neighbour]['time_stamp'], start_time)
            if position > 0:
                time = G[node][neighbour]['time_stamp'][position]
                if most_recent < time:
                    most_recent = time
                    aim_node = neighbour
        if aim_node not in random_list and aim_node != -1:  # 查询是否重复
            re.append(aim_node)
        else:
            re.append(node)
            count = count + 1  # 记录出现公共节点的次数
    sentinels = [re, count]
    return sentinels


def take_first(elem):
    return elem[0]


# [中位数联系策略] 选择连接度适当的节点（中位数），既不密集也不稀疏，可能是2B 返回两个哨兵节点集合
def mid_link(G, random_list, start_time):
    count = 0
    re = []
    for node in random_list:
        rank_list = []
        i = 0
        for neighbour in G[node]:
            times = binary_search(G[node][neighbour]['time_stamp'], start_time) + 1
            rank_list.append([times, i])
            i = i + 1
        rank_list.sort(key=take_first)  # 根据第一个元素进行排序
        aim_node = list(G[node])[rank_list[rank_list.__len__() // 2][1]]  # 选择中位数
        if aim_node not in random_list and not aim_node:  # 查询是否重复
            re.append(aim_node)
        else:
            re.append(node)
            count = count + 1  # 记录出现公共节点的次数
    sentinels = [re, count]
    return sentinels


# [度值最大策略] 对比作用,不作为哨兵策略，
def degree(G):
    degree_value = list(G.degree)
    degree_value = sorted(degree_value, key=lambda item: item[1], reverse=True)
    sentinels = []
    return degree_value


def strength(G):
    rank_list = []
    for node in G:
        count = 0
        for nbr in G[node]:
            count += len(G[node][nbr]['time_stamp'])
        rank_list.append([node, count])
    rank_list.sort(key=lambda x: x[1], reverse=True)
    return rank_list


# 返回除度值策略以外的哨兵集合
def get_sentinels(G, view_period, sentinel_rate):
    begin_pos = int(view_period * (len(G.graph['time_stamp_list'])))
    last_time = list(G.graph['time_stamp_list'])[begin_pos - 1]
    random_list = random_select(G, sentinel_rate)
    acquaintances_list = acquaintances(G, random_list)
    most_active_list = most_active(G, random_list, last_time)
    weighted_most_active_list = weighted_most_active(G, random_list, last_time, 0.8)
    recent_list = recent(G, random_list, last_time)
    mid_link_list = mid_link(G, random_list, last_time)
    # degree_list = degree(G, sentinel_rate)
    sentinels = [random_list, acquaintances_list[0], most_active_list[0], weighted_most_active_list[0],
                 recent_list[0], mid_link_list[0]]
    i = 0
    for item in sentinels:
        item.sort()
        sentinels[i] = tuple(item)
        i = i + 1
    return sentinels


def weighted_strength(G, time, loc, la):
    rank_list = []
    i = 0
    for node in G:
        score = 0
        for nbr in G[node]:
            for t in G[node][nbr]['time_stamp']:
                score += la * np.exp(la * (t - loc * time) / time)
        rank_list.append([node, score])
        rank_list.sort(key=lambda x: x[1], reverse=True)
        i += 1
    return rank_list
