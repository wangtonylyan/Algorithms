# -*- coding: utf-8 -*-

# Algorithmic Paradigm
# 【concurrency】
# philosopher
# 【parallelism】
# 【divide and conquer】
# binary search
# merge sort
# quick sort
# 【dynamic programming】
# knapsack
# 【greedy】


# 问题归类
# 【linear extension】
# a linear order (or total order) that is compatible with the partial order
# 即根据一个偏序得出一个与之并不矛盾的全序
# 此类问题有：拓扑排序；MRO

# 【从数的二进制表示，2^0+2^1+...+2^n=2^(n+1)-1】
# 二叉树中同时具有左右子树的节点个数一定等于该树叶子节点的个数减一
# 此类算法诸如：
# 1) 找到不小于一个数的2的幂，利用"位操作或"实现累加
# 2) 完全背包转换成0-1背包，利用"加法"实现累加
# 3) 后缀数组O(nlogn)的构造，利用"排序的稳定性"实现累加

# 【subsequence vs. substring】
# 需严格区分subsequence和substring这两个词
# 前者是指非连续的序列问题，后者则针对连续的字符串


# 技巧
# 【递归】
# 利用对于递归的调用与返回，形成了一次折返，极大地简化了数据结构的遍历
# 例如在以递归方式实现的红黑树中，可以将原本复杂的平衡算法拆分成两个部分
# 即在top-down和buttom-up阶段分别予以实现


# 关于红黑树的思考
# 根据红黑树的平衡算法得到的整棵二叉树不是完全平衡的
# 表现出的恰恰是一种"多样性"，虽局限于某个范围/限制内
