# 1. 算法原理

**适用场景** ： 牛顿法用于寻找目标函数的零点，当目标函数存在连续二阶导数时，也可以求解目标函数的极值；  

在运筹优化中用于求解无约束的非线性规划问题，如无约束的二次规划问题。 

## 1.1 **一维情况** ：

基本思想是初始化一个点，然后求导数做切线，逐渐迭代，如下图所示：

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/求解算法-04-牛顿法/图片附件/pic-1-一维牛顿法.jpg)

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/求解算法-04-牛顿法/图片附件/pic-2-一维牛顿法.jpg)

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/求解算法-04-牛顿法/图片附件/pic-3-一维牛顿法.jpg)

## 1.2 **二维及更高维度情况** ：  

如果需要求f(x)的极值，可以转换为求f'(x)的零点。在二维及更高维度下，迭代公式中用梯度向量和Hessian矩阵进行计算，如下图所示：

![i](https://github.com/zenghang-feng/operation_optimization/blob/main/求解算法-04-牛顿法/图片附件/pic-4-二维牛顿法.jpg)

给定一个二阶连续可导的目标函数，需要求此目标函数的极值，步骤如下：  

**第1步** ，设置一个随机初始化的向量；同时设置一个误差变量error，作为迭代终止条件，当梯度变化小于误差变量时，停止迭代；  

**第2步** ，计算目标函数在当前点的Hessian矩阵的逆，以及梯度向量，按照上文中的公式进行迭代；

**第3步**，计算迭代后的点对应目标函数的取值，与上一个点目标函数取值做差得到f_dif，f_dif与误差变量error比较，  

如果大于误差变量，则转入 **第2步** ，如果小于等于误差变量，则终止算法，返回最优点对应函数值。


**极值判断** ，首先计算Hessian矩阵，并计算矩阵的特征值，判断各个特征值的正负，如果特征值全部大于0，是极小值，  

如果特征值全部小于0，是极大值。

# 2. 程序实现
```
import sympy as sp

#################################################################
# 定义目标函数，并计算hessian矩阵特征值
#################################################################
# 定义变量、函数 ===================================================
x, y = sp.symbols(["x", "y"])
f_xy = x**4 + 0.8 * y**4 + 4 * x**2 + 2 * y**2 - x * y - 0.2 * x ** 2 * y

#################################################################
# 牛顿法求极值
#################################################################
# 初始化选择一个点 =================================================
vec_k = sp.Matrix([5, 6])
point_list = []
point_list.append(vec_k)

# 定义用于判断终止条件的误差 =========================================
error = 0.001
f_dif = 100

# 计算梯度和hessian矩阵 ============================================
grad = sp.Matrix([sp.diff(f_xy, x), sp.diff(f_xy, y)])       # 计算梯度
hessian = sp.hessian(f_xy, varlist=[x, y])                                    # 计算Hessian矩阵

# 开始进行迭代 ====================================================
c = 0
while f_dif > error:
    x_k = vec_k[0, 0]
    y_k = vec_k[1, 0]
    f_xy_k_val = f_xy.subs([(x, x_k), (y, y_k)])

    grad_val = grad.subs([(x, x_k), (y, y_k)])
    hessian_val = hessian.subs([(x, x_k), (y, y_k)])
    hessian_val_inv = hessian_val.inv()
    vec_k1 = vec_k - hessian_val_inv * grad_val

    x_k1 = vec_k1[0,0]
    y_k1 = vec_k1[1,0]
    f_xy_k1_val = f_xy.subs([(x,x_k1), (y,y_k1)])

    f_dif = abs(f_xy_k_val-f_xy_k1_val)
    vec_k = vec_k1

    c += 1
    print(c, "次迭代")

#################################################################
# 计算特征值，判断是极大值还是极小值 ==================================
#################################################################
eigen_values = hessian_val.eigenvals()
# 特征值均为正数，所以极值点是极小值


```

# 3. 牛顿法的问题

问题主要有：目标函数需要有一阶、二阶导数，Hessian矩阵求逆的运算很大等
