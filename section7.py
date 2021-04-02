"""
# @Author  : wujiayun
# @Date    : 2021/3/30 11:39
# @File    : section7.py
"""
import init_net as init
import numpy as np
import networkx as nx
import progressbar
import matplotlib.pyplot as plt


def global_node_marking(network_file, simulation_file, time_windows):
    g = nx.Graph
    g = init.init(network_file)
    simulation = np.load(simulation_file, allow_pickle=True)
    node_score_table = np.empty([len(g), 4], dtype='float')
    nodes = np.array(list(g.nodes))
    nodes_time_list = [[] for row in range(len(nodes))]
    nodes_public_list = [[] for row in range(len(nodes))]
    node_score_table[:, 0] = nodes
    count = 0
    progress = 0
    break_size = []
    with progressbar.ProgressBar(max_value=len(simulation)) as bar:
        for sir in simulation:
            progress += 1
            if len(sir) > 1:
                count += 1
                break_size.append(len(sir))
                for i in range(1, len(sir)):
                    p = np.where(nodes == sir[i][0])
                    time = (sir[i][1] - sir[0][1]) / time_windows
                    public = i / (len(sir) - 1)
                    nodes_time_list[p[0][0]].append(time)
                    nodes_public_list[p[0][0]].append(public)
            bar.update(progress)
    mean = np.mean(break_size)
    for loc in range(len(nodes)):
        avg_likelihood = len(nodes_public_list[loc]) / count
        avg_time = np.mean(nodes_time_list[loc])
        avg_public = np.mean(nodes_public_list[loc])
        node_score_table[loc, 1] = avg_likelihood
        node_score_table[loc, 2] = avg_time
        node_score_table[loc, 3] = avg_public
    plt.figure(dpi=300)
    indicator = ['DL', 'DT', 'PA']
    x = np.arange(1, len(nodes) + 1, 1)
    plt.title(network_file.split("\\")[-1].split('.')[0])
    for i in range(1, 4, 1):
        plt.subplot(3, 1, i)
        plt.scatter(x, node_score_table[:, i], s=1)
        plt.ylabel(indicator[i - 1])
    plt.show()


global_node_marking('G:\\sentinel\\networks\\dating\\dating4.csv',
                    "G:\\sentinel\\simulation data\\dating4\\beta0.5niu0.5.npy", 44236115//6)
