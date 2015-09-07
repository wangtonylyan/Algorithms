#problem: exchange two object
#solution: use no additional space
#此算法并不推荐，要求数据结构必须支持加减法运算
# 使用一个额外辅助变量的方式已经足够优化了
def exchange((i, j)):
    i = i + j
    j = i - j
    i = i - j
    return (i, j)

print exchange((1,2))