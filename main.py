#problem: exchange two object
#solution: use no additional space
#���㷨�����Ƽ���Ҫ�����ݽṹ����֧�ּӼ�������
# ʹ��һ�����⸨�������ķ�ʽ�Ѿ��㹻�Ż���
def exchange((i, j)):
    i = i + j
    j = i - j
    i = i - j
    return (i, j)

print exchange((1,2))