import numpy as np


#################################################################
# 定义优化目标: maximize obj: (40-2*x) * (30-2*x) * x
#################################################################
# 目标函数化简之后：f = 4 * x**3 - 140 * x**2 + 1200 * x
def f(x):
    return 4 * x ** 3 - 140 * x ** 2 + 1200 * x


# 自变量取值范围 ==================================================
x_low = 0
x_up = 15

#################################################################
# 遗传算法
#################################################################
# 定义算法所需的超参数 =============================================
L = 300             # 算法迭代次数
size = 50           # 种群大小
p_c = 0.7           # 交叉概率
p_v = 0.01          # 变异概率

# 根据自变量取值范围，随机采样生成规模为size的初始种群 ===================
# 对于每个样本来说，采样的是一个浮点数作为编码方式，也无需解码 -------------
list_samp = np.random.uniform(low=x_low, high=x_up, size=size)
list_index = list(range(size))

# 定义适应度函数，这里适应度函数就是目标函数 ============================
fitness = f


for l in range(L):
    # 计算各个样本的适应度 -----------------------------------------
    list_fit_val = [fitness(x) for x in list_samp]
    
    # 轮盘筛选父代样本，形成新的种群 ---------------------------------
    fit_val_sum = sum(list_fit_val)
    s = 0
    list_samp_sub = []
    while s < size:
        ind = np.random.choice(a=list_index, size=1)[0]               # 随机从种群中筛选索引
        if list_fit_val[ind]/fit_val_sum > np.random.rand():
            list_samp_sub.append(list_samp[ind])
            s += 1

    # 从新生成的种群中按照概率p_c筛选样本进行交叉操作 --------------------    # 交叉操作的写法可以进一步优化
    list_samp_cross = []
    list_samp_no_cross = []
    for i in range(size):
        if np.random.rand() < p_c:
            list_samp_cross.append(list_samp_sub[i])
        else:
            list_samp_no_cross.append(list_samp_sub[i])
    length_cross = len(list_samp_cross) // 2
    for i in range(length_cross):
        s_max = max(list_samp_cross[i], list_samp_cross[i*2])
        s_min = min(list_samp_cross[i], list_samp_cross[i*2])
        list_samp_cross[i] = (s_max + s_min) / 2
        list_samp_cross[i*2] = (0.5 * s_max + 1.5 * s_min) / 2
    list_samp_sub = list_samp_cross + list_samp_no_cross

    # 从新生成的种群中按照概率p_v筛选样本进行交叉操作 ---------------------
    for i in range(size):
        if np.random.rand() < p_v:
            list_samp_sub[i] = np.random.uniform(low=x_low, high=x_up)

    list_samp = list_samp_sub
    print('迭代次数', l)

x_best = list_samp[0]
y_best = fitness(list_samp[0])
for s in list_samp:
    y_tmp = fitness(s)
    if y_tmp > y_best:
        x_best = s
        y_best = y_tmp

print('最优解对于x是', x_best, '最优解的值是', y_best)
