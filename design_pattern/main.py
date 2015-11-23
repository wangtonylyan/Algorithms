# design pattern: reusability, flexibility


# object diagram：处理对象之间的关系，决定于运行期。
# class diagram：处理类的关系，决定于在编译期。
# interaction diagram：

# classification by two criteria: purpose(creational,structural,behavioral) & scope(class,object)
# 1) creational class pattern & creational object pattern
# 主要作用是用于创建对象
# The creational class patterns defer some part of object creation to subclasses,
# while the creational object patterns defer it to another object.
# 2) structural class pattern & structural object pattern
# 主要作用是以不同的子对象来组建更大规模的对象结构
# The structural class patterns use inheritance to compose classes,
# while the structural object patterns describe ways to assemble objects.
# 3) behavioral class pattern & behavioral object pattern
# 主要作用是用于管理对象（或其之间）的算法、关系、职责
# The behavioral class patterns use inheritance to describe algorithms and flow of control,
# whereas the behavioral object patterns describe how a group of objects cooperate to
# perform a task that no single object can carry out alone.

# 很多设计模式都是针对于静态语言的，而动态语言中的一些语法特性（或静态语言中的动态特性）可以很好地替代设计模式

# 设计模式可以针对于：1)单个类的设计，2)类之间的关联/组合，3)同一个继承树上的类的设计


# the testcase method in each design pattern class illustrates the actions of client as the pattern's user


# creational pattern: singleton, prototype, factory method, abstract factory, builder
# structural pattern: proxy, decorator, facade, adapter
# behavioral pattern: template method,


# 很多模式的目的都在于要避免继承，因为继承的层次过深会引入额外的复杂度
# 例如proxy、decorator、adapter、delegate


# class inheritance & object composition
# the former breaks encapsulation and changes behavior at compiler time
# the later keeps encapsulation and remains in run time
# Favor object composition over class inheritance.
