# 1. 问题描述
有3个货物需要从A地运输到B地，货物的重量如下所示：  

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/02-整数规划-物流组合方案/图片附件/pic1.png)

现在有6种可以选择的物流服务，前3种物流服务是专车运输，每种专车的载重和费用如下所示；后3种物流服务是散件运输，每种散件运输的首重及后续单价如下所示：  

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/02-整数规划-物流组合方案/图片附件/pic2.png)

问每个货物采用怎样的运输方式，可以以最低的总成本将这3件货物运输到目的地？（每个货物只能采用一种物流服务，不同的货物可以采用同一种物流服务）

# 2. 问题分析
这个问题可以作为一种组合优化（整数规划）的问题处理，通过如下的方式建立每个货物和每种物流服务的联系。  

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/02-整数规划-物流组合方案/图片附件/pic3.png)

## 2.1 定义变量
定义变量x00 - x25，这些变量的取值为0或1，以x00为例，x00=1，代表货物1采用物流服务1(专车1)运输，x00=0，代表货物1没有采用物流服务1(专车1)运输。   

定义变量n1 - n3，代表专车1、专车2、专车3这3种物流服务最终实际使用的车的数量，n1、n2、n3均为取值大于等于0的正整数；  

定义变量y1 - y6，代表每一种物流服务实际的物流费用，y1、y2、y3、y4、y5、y6的取值为大于等于0的正数；

## 2.2 定义优化目标
优化目标由每一种物流服务实际的物流费用组成，对于专车运输的3种服务，每一种服务的物流费用为 实际用车数量 x 每一辆车的单价；  

对于散件运输的3种服务，每一种服务的物流费用为 首重金额 + (超出首重的重量 x 单价)；  

因此可以定义优化目标如下：  

Minimize obj: y1 + y2 + y3 + y4 + y5 + y6

## 2.3 定义约束条件
对于每个货物来说，每种货物最终只能采用一种物流服务，所以有如下约束：  

x11 + x12 + x13 + x14 + x15 + x16 = 1  

x21 + x22 + x23 + x24 + x25 + x26 = 1  

x31 + x32 + x33 + x34 + x35 + x36 = 1  

对于每种物流服务来说，最终实际的载重(专车的物流服务才有载重约束)和最终实际的物流费用有如下约束：  

100 * x10 + 50 * x20 + 180 * x30 <= 200 * n1  

100 * x11 + 50 * x21 + 180 * x31 <= 80 * n2  

100 * x12 + 50 * x22 + 180 * x32 <= 50 * n3  

y1 = 150 * n1  

y2 = 80 * n2  

y3 = 50 * n3  

y4 = 10 + (100 * x14 + 50 * x24 + 180 * x34 - 50) * 2  

y5 = 8 + (100 * x15 + 50 * x25 + 180 * x35 - 10) * 1.5  

y6 = 6 + (100 * x16 + 50 * x26 + 180 * x36 - 5) * 1  

对于每个变量来说，取值有如下约束：  

xij 取值为0或1，i=1,2,3; j=1,2,3,4,5,6  

nj取值为大于等于0的正整数，j=1,2,3  

# 3. 程序实现
```
# 参考链接：https://zhuanlan.zhihu.com/p/623360039
# 导入docplex
from docplex.mp.model import Model
import pandas as pd

##############################################################################
# 创建模型对象
##############################################################################
op = Model()

##############################################################################
# 定义变量：Xij是0-1类型变量；Tk是每种服务的重量求和结果，转换为的整数值；Yk是每个服务下产生的物流费用
##############################################################################
d = 3                                                               # 发货需求的数量
s1 = 3                                                              # 专车类型的物流服务的数量
s2 = 3                                                              # 散件类型的物流服务的数量
s_all = s1 + s2

d_list = ['发货需求' + str(i) for i in range(d)]
s_list = ['物流服务' + str(j) for j in range(s_all)]

var_01 = pd.DataFrame(index=d_list, columns=s_list)                 # 是0-1类型变量
for i in range(d):
    for j in range(s_all):
        var_01.iloc[i,j] = op.binary_var(name = 'x'+str(i)+str(j))

var_car_num = []                                                    # 每一种专车类型的物流服务的用车数量
var_tmp = []                                                        # 每一种物流服务组合之后的载重总量
var_cost = []                                                       # 每一种物流服务组合之后的总的运输费用
for j in range(s_all):
    j_str = str(j)
    if j < 3:
        var_car_num.append(op.integer_var(lb=0, ub=100, name='n'+j_str))
        
    var_tmp.append(op.continuous_var(lb=0, ub=op.infinity, name='t'+j_str))
    var_cost.append(op.continuous_var(lb=0, ub=op.infinity, name='y'+j_str))

##############################################################################
# 定义参数：
##############################################################################
# 定义发货需求对应的货物重量参数
coeff_d = [100, 50, 180]                                            # 每个发货需求对应的货物的重量

# 定义物流服务为专车的参数
coeff_s1_cap = [200, 100, 50]                                       # 每个专车类型的物流服务对应的车辆载重
coeff_s1_fee = [150, 80, 50]                                        # 每个专车类型的物流服务对应的车辆总费用

# 定义物流服务为散件的参数：分段函数列表（colex规定的格式如下）
coeff_s2_pwl = [[0, [(0,0), (0.000001,10), (50,10)], 2.0], [0, [(0,0), (0.000001,8), (10,8)], 1.5], [0, [(0,0), (0.000001,6), (5,6)], 1.0]]

##############################################################################
# 定义优化目标: Minimize obj: y1 + y2 + y3 + y4 + y5 + y6
##############################################################################
obj = op.sum(y for y in var_cost)
op.minimize(obj)

##############################################################################
# 定义约束条件
##############################################################################
# 添加对发货需求的约束
for i in range(d):
    op.add_constraint(ct = op.sum(var_01.iloc[i, j] for j in range(s_all))==1, ctname='c_d'+str(i))

# 添加对发货需求和物流服务之间关系的约束：分段计费模型
for j in range(s_all):
    op.add_constraint(ct = op.sum(coeff_d[i] * var_01.iloc[i,j] for i in range(d)) - var_tmp[j] == 0, ctname='c_ds'+str(j))
    
    if j < 3:
        op.add_constraint(ct = var_tmp[j] - var_car_num[j] * coeff_s1_cap[j] <= 0, ctname='car_num'+str(j))
        op.add_constraint(ct = var_cost[j] - var_car_num[j] * coeff_s1_fee[j] == 0, ctname = 'car_fee'+str(j))
    
    else:
        j_fix = j - 3
        pwl = op.piecewise(coeff_s2_pwl[j_fix][0], coeff_s2_pwl[j_fix][1], coeff_s2_pwl[j_fix][2])
        op.add_piecewise_constraint(y=var_cost[j], pwlf=pwl, x=var_tmp[j], name='pwl'+str(j))

##############################################################################
# 求解优化问题
##############################################################################
solution = op.solve()

# 获取最优结果
if solution:
    # 输出优化目标的计算结果
    print(f"最优值为：{op.objective_value:.2f}")

    # 输出各个变量的计算结果
    res_dit_best = {}
    for i in range(d):
        for j in range(s_all):
            res_dit_best['x'+str(i)+str(j)] = var_01.iloc[i,j].solution_value
else:
    print("求解失败")

"""
# 获取全部结果集合
res_pool = op.populate_solution_pool()
res_list = [s for s in res_pool._solutions]
res_list_all = []
for i, s in enumerate(res_list):
    tmp = []
    tmp.append(s.objective_value)

    # s.get_value(var_01.iloc[0, 0])
    # tmp.append(s._var_value_map)
    # 以下为最新提前变量和变量取整的程序
    # dit_var = {}
    lis_var = []
    dit_tmp = s._var_value_map
    for k in dit_tmp:
        # dit_var[k.name] = dit_tmp[k]
        lis_var.append([k.name, dit_tmp[k]])
        df_var = pd.DataFrame(lis_var)
        df_var.columns = ['变量名称', '变量取值']
    tmp.append(df_var)
    res_list_all.append(tmp)

"""
```

求解的结果如下：

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/02-整数规划-物流组合方案/图片附件/pic_res.png)
