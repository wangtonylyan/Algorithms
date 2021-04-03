# LeetCode


## Array
1. 121
   题目121，似乎可以用滑动窗口的思想来理解，有待确认？


## Dynamic Programming
1. 70, 746, 53, 300, 198, 213
2. 120, 62, 63, 64, 221, 256, 265, 国王与金矿

采用二维动态规划的问题，通常存在有两个不同维度上的子问题
此时需要二维数组，分别解决不同维度上的子问题
比较天然的二维有：二维空间中的移动，包括二维网格


## dp[i]可以存储两种结果，
## 即input[i]的瞬间结果，例如子序列中包含当前字符、当前房子被偷、空间遍历到达点
## 以及input[:i]的累积结果
## 根据将input[i]加入input[:i]时，所需面对的情况，来选择记录哪种结果
# 1. 采用前者
# 1.1. 目标就是求出input[-1]时的瞬间结果，此时的dp[-1]往往就是最终结果
#      例如：阶梯问题(1, 1_1)，单个终点的遍历路径
# 1.2. 目标是求出某个input[i]时的瞬间结果，而并不严格地依赖于input[-1]
#      此外，仅根据input[i]又难以从input[:i]中得出累计结果
#      例如：子序列问题(2, 2_1, 3)，多个终点的遍历路径
# 2. 采用后者
# 2.1.


## Greedy


连续子序列

1. 对于连续性

从递归的角度，lst[i]要么紧接lst[i-1]，要么作为一个新子序列的首项

连续子序列并不以原序列的末项为结尾，即连续子序列可以任意某项为末项，
因此此类问题需要记录整个序列各项上的中间结果，反而不利于递归实现，
反之，目前都挺容易使用递归实现的。


如何判断一个数组中的元素都相同
如何判断一个数组中存在有或没有重复元素






## 温故算法
1. 排序
2. 二叉树
   是否完全、是否平衡
   最近公共祖先