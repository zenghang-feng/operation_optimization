**适用场景** ：求解线性规划问题（优化目标、约束条件均为线性函数，变量取值均为连续数值）

# 1. 算法原理

**前置条件** ：线性规划的最优解一定位于角点。  

**标准形式** ：  

1）所有的约束都是等式（变量的非负限制除外），并且具有非负的右端项。  

2）所有变量是非负的。  

备注：可以引入松弛变量达到上述效果。  

问题：等式约束中没有松弛变量的情况，需要用大M方法、两阶段方法处理。  

**最优性条件** ：在极大化（极小化）问题中，进基变量是z行中具有最负（最正）系数的非基变量。如果有多个可任选其一。  

当非基变量的所有z行系数是非负的（非正的）时，迭代达到最优值。  

**可行性条件** ：对于极大化和极小化问题，离基变量都是具有最小非负比（带有严格的正分母）的基变量。如有多个可任选其一。  

**高斯-若尔当行运算** ：  

1）枢轴行  

a. 在基列中，用进基变量替换离基变量。  

b. 新的枢轴行 = 当前枢轴行 ➗ 枢轴元素  

2）包括 z 的所有其他行

新行 = 当前行 - 枢轴列系数 ✖ 新的枢轴行

**单纯形法的步骤** ：  

第1步 确定初始基本可行解；  

第2步 用最优性条件选择一个进基变量。如果没有进基变量，停止计算；上一个解就是最优的。否则，转到第3步；

第3步 用可行性条件选择离基变量；

第4步 用适当的高斯-若尔当 行运算确定新的基本解，转到第2步；

