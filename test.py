import numpy as np
import math
import random
import tiles as t

# 验证指数分布是否相同：结果 属于相同分布
# for i in range(10):
#     r = np.random.randint(0, 2147483647)
#     exp = -10 * np.log((r+1)/2147483647)
#     # exp = exp/10
#     # r += int(exp)
#     exp = int(exp)
#     print(exp)
#
# print('----------')
# for i in range(100):
#     exp = int(np.random.exponential(10))
#     # exp = exp/100
#     # l += exp
#     print(exp)
#
# 测试结果 少了一次
# now = np.array(np.random.geometric(0.1, 1000))
# print('xixi')
# old = []
# for i in range(10):
#     print(int((math.log(1 - random.random())) / (math.log(1 - 0.1))))
#     print(np.random.geometric(0.1))

tl = t.TILES("G:\\sentinel\\networks\\prostitution.csv", obs=2232)
tl.execute()