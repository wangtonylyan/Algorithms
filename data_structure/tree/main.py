# -*- coding: utf-8 -*-

# 能用is就不用==，尤其对于Node类型
# 用于表示树结构的变量不用"is (not) None"判断，直接使用"if (not)"
# 节点中的value值必须使用"is (not) None"来判断
# insert()的传参key和value必须都是"is not None"
