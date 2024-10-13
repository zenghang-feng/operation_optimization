import numpy as np

#################################################################
# 定义优化目标: maximize obj: (40-2*x) * (30-2*x) * x
#################################################################
# 目标函数化简之后：f = 4 * x**3 - 140 * x**2 + 1200 * x
def f(x):
    return 4 * x ** 3 - 140 * x ** 2 + 1200 * x

# 定义算法相关的超参数 =============================================
T_start = 100
T_end = 1
L_at_T = 100
r_atten = 0.998
k = 1

# 初始化自变量，是0-15区间随机一个数值 ================================
x = 15 * np.random.rand()
# 初始化温度，取值为T_start =========================================
T = T_start

# 开始算法迭代 =====================================================
while T > T_end:
    for i in range(L_at_T):
        x_new = x + np.random.uniform(low=-1, high=1, size=1)[0]
        if 0 < x_new < 15:
            f_dif = f(x_new) - f(x)
            if f_dif > 0:
                x = x_new
            else:
                p_de = np.exp(f_dif/(k*T))
                if p_de > np.random.rand():
                    x = x_new
                else:
                    pass
        else:
            pass
    T = T * r_atten

print("最优解对应的x", x, "最优解", f(x))