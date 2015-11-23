# design pattern: reusability, flexibility


# object diagram���������֮��Ĺ�ϵ�������������ڡ�
# class diagram��������Ĺ�ϵ���������ڱ����ڡ�
# interaction diagram��

# classification by two criteria: purpose(creational,structural,behavioral) & scope(class,object)
# 1) creational class pattern & creational object pattern
# ��Ҫ���������ڴ�������
# The creational class patterns defer some part of object creation to subclasses,
# while the creational object patterns defer it to another object.
# 2) structural class pattern & structural object pattern
# ��Ҫ�������Բ�ͬ���Ӷ������齨�����ģ�Ķ���ṹ
# The structural class patterns use inheritance to compose classes,
# while the structural object patterns describe ways to assemble objects.
# 3) behavioral class pattern & behavioral object pattern
# ��Ҫ���������ڹ�����󣨻���֮�䣩���㷨����ϵ��ְ��
# The behavioral class patterns use inheritance to describe algorithms and flow of control,
# whereas the behavioral object patterns describe how a group of objects cooperate to
# perform a task that no single object can carry out alone.

# �ܶ����ģʽ��������ھ�̬���Եģ�����̬�����е�һЩ�﷨���ԣ���̬�����еĶ�̬���ԣ����Ժܺõ�������ģʽ

# ���ģʽ��������ڣ�1)���������ƣ�2)��֮��Ĺ���/��ϣ�3)ͬһ���̳����ϵ�������


# the testcase method in each design pattern class illustrates the actions of client as the pattern's user


# creational pattern: singleton, prototype, factory method, abstract factory, builder
# structural pattern: proxy, decorator, facade, adapter
# behavioral pattern: template method,


# �ܶ�ģʽ��Ŀ�Ķ�����Ҫ����̳У���Ϊ�̳еĲ�ι�����������ĸ��Ӷ�
# ����proxy��decorator��adapter��delegate


# class inheritance & object composition
# the former breaks encapsulation and changes behavior at compiler time
# the later keeps encapsulation and remains in run time
# Favor object composition over class inheritance.
