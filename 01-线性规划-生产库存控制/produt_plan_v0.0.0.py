# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:57:23 2024

@author: fengzenghang
"""

from docplex.mp.model import Model

# 创建模型对象
op = Model()

# 定义变量：x_i，s_j均为连续型数值变量
var_dit = {}
var_name_list = ['x1', 'x2', 'x3', 'x4', 's1', 's2', 's3', 's4']
for v in var_name_list:
    var_dit[v] = op.continuous_var(lb=0, name=v)

# 定义优化目标: maximize obj: 30*x1 + 40*x2 + 20*x3 + 10*x4 - 15*s1 - 20*s2 - 10*s3 - 8*s4
op.maximize(30*var_dit['x1'] + 40*var_dit['x2'] + 20*var_dit['x3'] + 10*var_dit['x4'] - 15*var_dit['s1'] - 20*var_dit['s2'] - 10*var_dit['s3'] - 8*var_dit['s4'])

# 添加约束条件
# c1：0.30*x1 + 0.30*x2 + 0.25*x3 + 0.15*x4 <= 1000
op.add_constraint(0.30*var_dit['x1'] + 0.30*var_dit['x2'] + 0.25*var_dit['x3'] + 0.15*var_dit['x4'] <= 1000)
# c2: 0.25*x1 + 0.35*x2 + 0.30*x3 + 0.10*x4 <= 1000
op.add_constraint(0.25*var_dit['x1'] + 0.35*var_dit['x2'] + 0.30*var_dit['x3'] + 0.10*var_dit['x4'] <= 1000)
# c3: 0.45*x1 + 0.50*x2 + 0.40*x3 + 0.22*x4 <= 1000
op.add_constraint(0.45*var_dit['x1'] + 0.50*var_dit['x2'] + 0.40*var_dit['x3'] + 0.22*var_dit['x4'] <= 1000)
# c4: 0.15*x1 + 0.15*x2 + 0.10*x3 + 0.05*x4 <= 1000
op.add_constraint(0.15*var_dit['x1'] + 0.15*var_dit['x2'] + 0.10*var_dit['x3'] + 0.05*var_dit['x4'] <= 1000)
# c5: x1 + s1 == 800
op.add_constraint(var_dit['x1'] + var_dit['s1'] == 800)
# c6: x2 + s2 == 750
op.add_constraint(var_dit['x2'] + var_dit['s2'] == 750)
# c7: x3 + s3 == 600
op.add_constraint(var_dit['x3'] + var_dit['s3'] == 600)
# c8: x4 + s4 == 500
op.add_constraint(var_dit['x4'] + var_dit['s4'] == 500)

# 求解优化问题
solution = op.solve()

# 获取结果
if solution:
    # 输出优化目标的计算结果
    print(f"最优值为：{op.objective_value:.2f}")

    # 输出各个变量的计算结果
    res_dit = {}
    for k in list(var_dit.keys()):
        res_dit[k] = var_dit[k].solution_value
else:
    print("求解失败")

