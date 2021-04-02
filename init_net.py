#  初始化网络以及基本分析
from collections import defaultdict
import networkx as nx
import numpy as np
from scipy import stats
import time


def init(filename):  # [初始化网络] 返回的G包含时序网络的所有信息，时间戳信息以list形式存储在edge上 时间戳根据CSV文件都是有序的，这里没有处理
    begin = time.time()
    time_stamp_list = []  # 存放时间戳列表 由于CSV文件的都是按时间戳升序，判断是否重复只需要判断最后一位
    G = nx.Graph(networks_name=(filename.split('.')[0]).split('\\')[-1], time_stamp_list=time_stamp_list)  # 以图的形式存储网络
    for line in open(filename, encoding='UTF-8'):  # 读取CSV网络文件
        str_list = line.split()
        n1 = int(str_list[0])  # 节点1
        n2 = int(str_list[1])  # 节点2
        n3 = int(str_list[2])  # 时间戳
        edge = (n1, n2)
        G.add_node(n1)
        G.add_node(n2)
        if len(time_stamp_list) == 0 or time_stamp_list[-1] != n3:  # 技巧 如果该if第二局在前第一次的时候会发生列表越界
            time_stamp_list.append(n3)
        # 以下方法将时间戳信息添加到edge上
        if G.has_edge(n1, n2):  # 两节点有边在此基础追加
            G.edges[n1, n2]['time_stamp'].append(n3)
        else:
            G.add_edges_from([edge], time_stamp=[n3])
    temp = list(G.nodes)
    for i in range(len(G.nodes)):  # 添加节点信息描述
        G.nodes[temp[i]]['state'] = []  # 节点的感染事件堆，里面存放二元组（感染时间，持续时间）
    # 全部初始化为易感节点
    del temp
    end = time.time()
    print((filename.split('.')[0]) + ' 网络生成完毕 time:' + str(int(end - begin)) + 's')
    return G


# [网络的基础分析]
def network_analyze_basic(G):
    degree = nx.degree_histogram(G)
    # x = range(len(degree))
    # y = [z / float(sum(degree)) for z in degree]
    # plt.title("degree distribution of " + G.graph['networks_name'])
    # plt.loglog(x, y, '.')
    # plt.savefig('G:\\figs\\degree\\' + G.graph['networks_name'])
    # 网络平均度值
    mean = np.mean(degree)
    print('平均度值：' + str(mean))
    # 节点总数
    node_num = len(G.nodes)
    print('节点总数:' + str(node_num))
    # 边总数（静态）
    edge_num = len(G.edges)
    print('边总数:' + str(edge_num))
    # 链接总数
    all_link_num = 0
    for edge in G.edges.data():
        all_link_num += len(edge[2]['time_stamp'])
    print('链接总数：' + str(all_link_num))
    # 网络稀疏度
    sparsity = all_link_num / (edge_num * len(G.graph['time_stamp_list']))
    print('稀疏度:' + str(sparsity))


def network_describer(filename):
    T = 0  # 最大时间戳
    contact_num = 0
    edge_temp = []
    time_stamp = set()  # 存储所有时间戳（联系的时间点）
    all_node = set()  # 存储所有节点
    half_contact_node = set()
    half_time_node = set()
    all_link = set()  # 存储所有边
    half_contact_link = set()
    half_time_link = set()
    G = nx.Graph()  # 以图的形式存储网络

    first_five_pre_contact_node = set()
    last_five_pre_contact_node = set()
    first_five_pre_time_node = set()
    last_five_pre_time_node = set()
    first_five_pre_contact_link = set()
    last_five_pre_contact_link = set()
    first_five_pre_time_link = set()
    last_five_pre_time_link = set()
    interevent_time_link = []
    interevent_time_node = []

    # simulation data = pd.read_csv(filename)
    # for i in range(len(simulation data) - 1):
    #     print(i)
    #     # strlist = line.split()
    #     n1 = simulation data['baseID2'][i]
    #     n2 = simulation data['baseID2'][i + 1]
    #     n3 = simulation data['start_date'][i + 1]
    #     if simulation data['ID'][i] == simulation data['ID'][i + 1]:
    #         edge = (n1, n2)
    #         temp = (edge, n3)
    #         edge_temp.append(temp)
    #         time_stamp.add(n3)
    #         all_node.add(n1)
    #         all_node.add(n2)
    #         all_link.add(edge)
    #         G.add_edges_from([(n1, n2)])
    #     if n3 > T:
    #         T = n3
    time_stamp_list = []
    for line in open(filename, encoding='UTF-8'):  # 读取CSV网络文件
        str_list = line.split()
        n1 = int(str_list[0])  # 节点1
        n2 = int(str_list[1])  # 节点2
        n3 = int(str_list[2])  # 时间戳
        edge = (n1, n2)
        G.add_node(n1)
        G.add_node(n2)
        if len(time_stamp_list) == 0 or time_stamp_list[-1] != n3:  # 技巧 如果该if第二局在前第一次的时候会发生列表越界
            time_stamp_list.append(n3)
        # 以下方法将时间戳信息添加到edge上
        if G.has_edge(n1, n2):  # 两节点有边在此基础追加
            G.edges[n1, n2]['time_stamp'].append(n3)
        else:
            G.add_edges_from([edge], time_stamp=[n3])
    all_node = list(all_node)
    all_node_num = len(all_node)
    all_link = list(all_link)
    all_link_num = len(all_link)
    contact_num = len(edge_temp)
    half_contact_num = int(0.5 * contact_num)  # half of the contacts
    # half_T = int(0.5 * T)  # half the sampling time
    half_T = int(T / 1000000)
    half_T = half_T * 1000000 + 120000
    # half_T = int(20200501120000)
    first_five_pre_contact = int(0.1 * contact_num)
    last_five_pre_contact = int(0.9 * contact_num)
    # first_five_pre_time = int(0.1 * T)
    first_five_pre_time = half_T
    # last_five_pre_time = int(0.9 * T)
    last_five_pre_time = half_T
    graph_Link_time = defaultdict(set)
    graph_Node_time = defaultdict(set)

    for i in range(contact_num):
        edge_te = edge_temp[i]
        edge = edge_te[0]  # 边
        edge_time = edge_te[1]  # 边的时间
        n1 = edge[0]
        n2 = edge[1]
        if i < half_contact_num:
            half_contact_node.add(n1)
            half_contact_node.add(n2)  # 统计half of the contacts前的节点
            half_contact_link.add(edge)  # 统计half of the contacts前的边
        if edge_time <= half_T:
            half_time_node.add(n1)
            half_time_node.add(n2)  # 统计half the sampling time前的节点
            half_time_link.add(edge)  # 统计half the sampling time前的边

        if i <= first_five_pre_contact:
            first_five_pre_contact_node.add(n1)
            first_five_pre_contact_node.add(n2)  # 统计the first 5% of the contact的节点
            first_five_pre_contact_link.add(edge)  # 统计the first 5% of the contact的边
        if i >= last_five_pre_contact:
            last_five_pre_contact_node.add(n1)
            last_five_pre_contact_node.add(n2)  # 统计the last 5% of the contact的节点0
            last_five_pre_contact_link.add(edge)  # 统计the last 5% of the contact的边
        if edge_time <= first_five_pre_time:
            first_five_pre_time_node.add(n1)
            first_five_pre_time_node.add(n2)  # 统计the first 5% of the sampling time的节点
            first_five_pre_time_link.add(edge)  # 统计the first 5% of the sampling time的边
        if edge_time >= last_five_pre_time:
            last_five_pre_time_node.add(n1)
            last_five_pre_time_node.add(n2)  # 统计the last 5% of the sampling time的节点
            last_five_pre_time_link.add(edge)  # 统计the last 5% of the sampling time的边

        graph_Link_time[edge].add(edge_time)  # 统计边上的时间戳
        graph_Node_time[n1].add(edge_time)  # 统计节点上的时间戳
        graph_Node_time[n2].add(edge_time)

    # 计算并输出time evolution的参数：
    half_contact_node = list(half_contact_node)
    half_contact_node_num = len(half_contact_node)
    f_NC = half_contact_node_num / all_node_num
    half_time_node = list(half_time_node)
    half_time_node_num = len(half_time_node)
    f_NT = half_time_node_num / all_node_num
    half_contact_link = list(half_contact_link)
    half_contact_link_num = len(half_contact_link)
    f_LC = half_contact_link_num / all_link_num
    half_time_link = list(half_time_link)
    half_time_link_num = len(half_time_link)
    f_LT = half_time_link_num / all_link_num
    first_five_pre_contact_node = list(first_five_pre_contact_node)
    last_five_pre_contact_node = list(last_five_pre_contact_node)
    node_num = 0
    for i in range(len(last_five_pre_contact_node)):
        node = last_five_pre_contact_node[i]
        if node in first_five_pre_contact_node:
            node_num = node_num + 1
    F_NC = node_num / all_node_num
    first_five_pre_time_node = list(first_five_pre_time_node)
    last_five_pre_time_node = list(last_five_pre_time_node)
    node_num = 0
    for i in range(len(last_five_pre_time_node)):
        node = last_five_pre_time_node[i]
        if node in first_five_pre_time_node:
            node_num = node_num + 1
    F_NT = node_num / all_node_num
    first_five_pre_contact_link = list(first_five_pre_contact_link)
    last_five_pre_contact_link = list(last_five_pre_contact_link)
    link_num = 0
    for i in range(len(last_five_pre_contact_link)):
        link = last_five_pre_contact_link[i]
        if link in first_five_pre_contact_link:
            link_num = link_num + 1
    F_LC = link_num / all_link_num
    first_five_pre_time_link = list(first_five_pre_time_link)
    last_five_pre_time_link = list(last_five_pre_time_link)
    link_num = 0
    for i in range(len(last_five_pre_time_link)):
        link = last_five_pre_time_link[i]
        if link in first_five_pre_time_link:
            link_num = link_num + 1
    F_LT = link_num / all_link_num
    print('Time evolution:')
    print('f_NC:', f_NC)
    print('f_NT:', f_NT)
    print('f_LC:', f_LC)
    print('f_LT:', f_LT)
    print('F_NC:', F_NC)
    print('F_NT:', F_NT)
    print('F_LC:', F_LC)
    print('F_LT:', F_LT)
    print('\n')

    # 计算并输出link activity和node activity的参数：
    for temp in graph_Link_time:
        temp_link_time = list(graph_Link_time[temp])
        temp_link_time = sorted(temp_link_time)
        for i in range(len(temp_link_time)):
            j = i + 1
            if j < len(temp_link_time):
                diff = temp_link_time[j] - temp_link_time[i]
                interevent_time_link.append(diff)
    mu_Lt = np.mean(interevent_time_link)
    sigma_Lt = np.std(interevent_time_link, ddof=1)
    c_Lt = (sigma_Lt - mu_Lt) / (sigma_Lt + mu_Lt)
    gamma_Lt = stats.skew(interevent_time_link)
    print('mu_Lt:', mu_Lt)
    print('sigma_Lt', sigma_Lt)
    print('c_Lt:', c_Lt)
    print('gamma_Lt:', gamma_Lt)
    print('\n')

    for temp in graph_Node_time:
        temp_link_time = list(graph_Node_time[temp])
        temp_link_time = sorted(temp_link_time)
        for i in range(len(temp_link_time)):
            j = i + 1
            if j < len(temp_link_time):
                diff = temp_link_time[j] - temp_link_time[i]
                interevent_time_node.append(diff)
    mu_Nt = np.mean(interevent_time_node)
    sigma_Nt = np.std(interevent_time_node, ddof=1)
    c_Nt = (sigma_Nt - mu_Nt) / (sigma_Nt + mu_Nt)
    gamma_Nt = stats.skew(interevent_time_node)
    print('mu_Nt:', mu_Nt)
    print('sigma_Nt', sigma_Nt)
    print('c_Nt:', c_Nt)
    print('gamma_Nt:', gamma_Nt)
    print('\n')

    graph_link_time_num = []
    graph_Node_time_num = []
    for temp in graph_Link_time:
        graph_link_time_num.append(len(graph_Link_time[temp]))
    for temp in graph_Node_time:
        graph_Node_time_num.append(len(graph_Node_time[temp]))

    mu_Ltau = np.mean(graph_link_time_num)
    sigma_Ltau = np.std(graph_link_time_num, ddof=1)
    c_Ltau = sigma_Ltau / mu_Ltau
    gamma_Ltau = stats.skew(graph_link_time_num)
    print('mu_Ltau:', mu_Ltau)
    print('sigma_Ltau', sigma_Ltau)
    print('c_Ltau:', c_Ltau)
    print('gamma_Ltau:', gamma_Ltau)
    print('\n')

    mu_Ntau = np.mean(graph_Node_time_num)
    sigma_Ntau = np.std(graph_Node_time_num, ddof=1)
    c_Ntau = sigma_Ntau / mu_Ntau
    gamma_Ntau = stats.skew(graph_Node_time_num)
    print('mu_Ntau:', mu_Ntau)
    print('sigma_Ntau', sigma_Ntau)
    print('c_Ntau:', c_Ntau)
    print('gamma_Ntau:', gamma_Ntau)
    print('\n')

    # 输出网络的度分布
    degree = nx.degree_histogram(G)
    mu_k = np.mean(degree)
    sigma_k = np.std(degree, ddof=1)
    c_k = sigma_k / mu_k
    gamma_k = stats.skew(degree)
    print('Degree distribution:')
    print('mu_k:', mu_k)
    print('sigma_k:', sigma_k)
    print('c_k:', c_k)
    print('gamma_k:', gamma_k)
    print('\n')
    # 度分布图
    # x = list(range(len(degree)))
    # y = [z / float(sum(degree)) for z in degree]
    # plt.title('degree distribution', fontsize = 15)
    # plt.xlabel('K')
    # plt.ylabel('P(K)')
    # plt.scatter(x, y)
    # plt.loglog(x, y)
    # plt.show()
    # plt.savefig("F:\\OSSTNE\\test.png")

    # 网络静态指标
    print('Other static network descriptors:')
    print('N:', all_node_num)  # 网络的节点个数
    g_cluster = nx.clustering(G)
    ave_g_cluster = 0
    for k in g_cluster:
        ave_g_cluster = ave_g_cluster + g_cluster[k]
    ave_g_cluster = ave_g_cluster / all_node_num
    print('average_clustering_coefficient:', ave_g_cluster)  # 网络的平均聚类系数
    print('E:', all_link_num)  # 网络的边个数
    print('Contact_num:', contact_num)  # 网络的联系数（时间戳的数目）

    # 存储信息至文件

    with open('/simulation data\\discriber\\result.txt', 'a') as f:
        temp = [str(filename)]
        f.writelines(temp)
        f.write('\n')
        temp = ['Time evolution:']
        f.writelines(temp)
        f.write('\n')
        temp = ['f_NC:', '\t', str(f_NC)]
        f.writelines(temp)
        f.write('\n')
        temp = ['f_NT:', '\t', str(f_NT)]
        f.writelines(temp)
        f.write('\n')
        temp = ['f_LC:', '\t', str(f_LC)]
        f.writelines(temp)
        f.write('\n')
        temp = ['f_LT:', '\t', str(f_LT)]
        f.writelines(temp)
        f.write('\n')
        temp = ['F_NC:', '\t', str(F_NC)]
        f.writelines(temp)
        f.write('\n')
        temp = ['F_NT:', '\t', str(F_NT)]
        f.writelines(temp)
        f.write('\n')
        temp = ['F_LC:', '\t', str(F_LC)]
        f.writelines(temp)
        f.write('\n')
        temp = ['F_LT:', '\t', str(F_LT)]
        f.writelines(temp)
        f.write('\n')
        temp = ['Node and link activity:']
        f.writelines(temp)
        f.write('\n')
        temp = ['mu_Lt:', '\t', str(mu_Lt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['sigma_Lt:', '\t', str(sigma_Lt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['c_Lt:', '\t', str(c_Lt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['gamma_Lt:', '\t', str(gamma_Lt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['mu_Nt:', '\t', str(mu_Nt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['sigma_Nt:', '\t', str(sigma_Nt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['c_Nt:', '\t', str(c_Nt)]
        f.writelines(temp)
        f.write('\n')
        temp = ['gamma_Nt:', '\t', str(gamma_Nt)]
        f.writelines(temp)
        f.write('\n')

        temp = ['mu_Ltau:', '\t', str(mu_Ltau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['sigma_Ltau:', '\t', str(sigma_Ltau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['c_Ltau:', '\t', str(c_Ltau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['gamma_Ltau:', '\t', str(gamma_Ltau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['mu_Ntau:', '\t', str(mu_Ntau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['sigma_Ntau:', '\t', str(sigma_Ntau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['c_Ntau:', '\t', str(c_Ntau)]
        f.writelines(temp)
        f.write('\n')
        temp = ['gamma_Ntau:', '\t', str(gamma_Ntau)]
        f.writelines(temp)
        f.write('\n')

        temp = ['Degree distribution:']
        f.writelines(temp)
        f.write('\n')
        temp = ['mu_k:', '\t', str(mu_k)]
        f.writelines(temp)
        f.write('\n')
        temp = ['sigma_k:', '\t', str(sigma_k)]
        f.writelines(temp)
        f.write('\n')
        temp = ['c_k:', '\t', str(c_k)]
        f.writelines(temp)
        f.write('\n')
        temp = ['gamma_k:', '\t', str(gamma_k)]
        f.writelines(temp)
        f.write('\n')
        temp = ['Other static network descriptors:']
        f.writelines(temp)
        f.write('\n')
        temp = ['N:', '\t', str(all_node_num)]
        f.writelines(temp)
        f.write('\n')
        temp = ['average_clustering_coefficient:', '\t', str(ave_g_cluster)]
        f.writelines(temp)
        f.write('\n')

        temp = ['E:', '\t', str(all_link_num)]
        f.writelines(temp)
        f.write('\n')
        temp = ['Contact_num:', '\t', str(contact_num)]
        f.writelines(temp)
        f.write('\n')

    return

#
# G = init("G:\\sentinel\\networks\\sulan.csv")
# network_analyze_basic(G)
