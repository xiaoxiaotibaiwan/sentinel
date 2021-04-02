"""
2021年3月
生成不同比例段的最大度值策略和最强联系策略
"""

import strategy as stg
import init_net as init
import numpy as np
import io

net_location = "G:\\sentinel\\networks\\prostitution\\prostitution4-6.csv"
save_location = "G:\\sentinel\\sentinels data\\prostitution\\"
G = init.init("G:\\sentinel\\networks\\prostitution.csv")
np.savetxt(save_location + 'degree.csv', stg.degree(G), encoding='utf8', fmt='%d')
np.savetxt(save_location+'strength.csv', stg.strength(G), encoding='utf8', fmt='%d')
# for i in range(1, 7):
#     file = net_location+str(i)+'.csv'
#     G = init.init(file)
#     np.savetxt(save_location+'degree'+str(i)+'.csv', stg.degree(G), encoding='utf8', fmt='%d')
#     np.savetxt(save_location+'strength'+str(i)+'.csv', stg.strength(G), encoding='utf8', fmt='%d')
G = init.init(net_location)
np.savetxt(save_location+'degree4-6.csv', stg.degree(G), encoding='utf8', fmt='%d')
np.savetxt(save_location+'strength4-6.csv', stg.strength(G), encoding='utf8', fmt='%d')