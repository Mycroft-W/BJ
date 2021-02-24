# OOP面对对象编程

以模块化的思想解决工程问题

面向过程 VS 面向对象

OO：面向对象

OOA：面向对象的分析

OOD：面向对象的设计

OOI：面向对象的实现

OOP：面向对象编程

OOA-->OOD-->OOI：面向对象的实现过程

## 类 VS 对象

类：抽象的一个集合,侧重于共性

对象：具体,描述的是个体

类的内容：

方法,函数

属性,变量

```python
# 定义一个类
class Student()：
    name = "name" # 类属性
    age = 19
    # 类方法
    def sayHi(self):
        print("hello,world")
        return None

# 类的实例化
shili = Student()
# 调用实例
shili.sayHi()
```

### self

* self可以用别的名称
* self不是关键字

实例可以借用类属性。

### 访问类的属性

再累里面如果要强制访问类属性,则需要使用`__calss__`,(前后两个下划线),使用类调用

绑定类方法：定义类方法时,没有self参数,只能通过类访问

### 构造函数

类在实例化的时候, 执行一些基础性的初始化的工作

使用特殊的名称和写法,必须有第一个参数

在实例化的时候自动调用

不能有return

```python
class Student():

    def __init__(self):

```

## 面向对象的三大特征

* 继承
* 封装
* 多态

### 封装

* 对对象成员进行访问限制
* 封装的三个级别：
  * 公开,public
  * 受保护,protected
  * 私有,private
  * public,protected,private不是关键字
* 判断对象的位置
  * 对象内部
  * 对象外部
  * 子类中
* 私有
  * 私有成员是最高级别的封装,只能在当前类或对象中访问
  * 在成员前面添加两个下划线即可,如 __name
* 受保护的封装
  * 在类与子类中可以访问,在外部不行
  * 在成员前面添加一个下划线,如 _name
* 公开的
  * 没有任何操作,所有地方都可以访问

### 继承

* 子类可以使用父类定义的内容和行为
* 继承与被继承的概念
  * 父类,基类,,被继承的类
  * 子类,也叫派生类,有继承行为的类
  * 继承关系是is-a的关系
  * 所有的类都有一个父类
    * 如果没有,则默认为object的子类
    * 可以有多个父类
* 继承变量查找顺序
  * 从自身开始,向上查找
* 单继承和多继承
* 菱形继承/钻石继承
  * 使用super()解决,MRO 方法解析顺序

#### 构造函数的继承

* 构造函数默认继承

### 多态

* 多态就是同一个对象在不同情况下有不同的状态出现
* 多态不是语法,是一种设计思想
* 多态性：一种调用方式,不同的执行效果

#### Mixin设计模式

* 主要采用多继承方式对类的功能进行拓展（像插件一样)
* 使用Mixin实现多继承时要注意
  * 必须表示某一个单一功能,而不是某个物品
  * Mixin不能依赖于子类的实现
  * 子类即使没有继承这个Mixin类,也能工作
* 优点
  * 不对类进行修改的情况下,扩充功能
  * 可以方便的组织和维护不同功能组件的划分
  * 可以根据需要调整功能类的组合

### issubclass()

检测前一个类是否是第二个的子类,返回bool值

### isinstance()

 检测一个对象是否是一个类的实例

### hasattr()

检测一个属性是否属于一个类

### getattr

get attribute

### setattr

set attribute

### delattr

delete attribute

### dir

获取对象的成员列表

### 类的成员描述符（属性）

类的成员描述符是为了在类中对得的成员属性进行相关操作而创建的一种操作方式

* get：获取属性的操作
* set：修改或者添加属性操作
* delete：删除属性的操作

如果想使用类的成员描述符,

* 使用类的实现描述器
* 使用属性修饰符
* 使用property函数
  * property(fget, fset, fdel, doc)

```python
# peroperty案例
class Person():
    '''
    这里是说明文档
    '''
    def fget(self):
        return self._name * 2
    def fset(self, name):
        self._name = name.upper()
    def fdel(self):
        self._name = "NoName"
    name = property(fget, fset, fdel,"对name进行操作")


p1 = Person()
p1.name = "TuLing"
print(p1._name)
```

无论哪种修饰符都是为了对成员属性进行相应操作

* 类的方式,适合多个类中的多个属性共用一个描述符
* property,使用当前类中使用,可以控制一个类中多个属性
* 属性修饰符,使用与当前类中使用, 控制一个类中的一个属性

### 类的内置属性

双下滑线开头和结尾的属性。

### 类的常用魔术方法

魔术方法就是不需要人为调用的方法,在特定时刻自动触发

魔术方法的统一特征时方法名前后双下划线。

操作类

如：\_\_init\_\_：构造函数

\_\_new\_\_：对象实例化方法,此函数较为特殊

\_\_call\__：对象当函数时使用

\__str__：当对象被当作字符串使用时调用

\__repr__：返回字符串,面向程序员时使用

描述符相关

\__set__

\__get__

\__delete__

属性操作相关

\__getattr__：访问一个不存在的属性时触发

\__setattr__：对晨光属性进行设置时触发

​参数：

​self用来获取当前对象

​被设置的属性名称,以字符串形式出现

​需要对属性的名称设置的值

​作用：进行属性设置的时候进行验证或修改

​注意：在该方法中不能对属性直接进行赋值操作,否则死循环

运算类相关魔术方法

\__gt__：进行大于判断的时候触发

​参数：

​self

​第二个参数是第二个对象

​放回置可以是任意值,推荐布尔值

### 类对象的三种方法

实例方法：需要实例化才能使用的方法,使用过程中可能需要截止对象的的其他对象的方法完成

静态方法：无需实例化,通过类直接访问,使用@staticmethod修饰,不需要第一个参数表示自身或类

类方法：无需实例化,使用@classmethod修饰,类方法的第一个参数,一般命名为cls,区别于self

### 抽象类

抽象方法,没有具体实现内容的方法称为抽象方法

抽象方法的主要意义是规范了子类的行为和接口

抽象类的使用需要借助abc模块

import abc

抽象类：包含抽象方法的类叫做抽象类,通常称为ABC类

```python
# 抽象类的实现
import abc
# 声明一个类并指定当前类的元类
class Human(metaclass=abc.ABCMeta):
    # 定义一个抽象方法
    @abc.abstractmethod
    def smoking(self):
        pass
    # 定义类的抽象方法
    @abc.abstractclassmethod
    def drink():
        pass
    # 定义静态抽象方法
    @abc.abstractstaticmethod
    def play():
        pass
```

抽象类的使用：

* 抽象类可以包含一个抽象方法,也可以包含具体方法和属性
* 抽象类不允许实例化,必须被继承才可使用,子类必须实现所有继承的抽象方法
* 子类如果没有实现所有继承的抽象方法,则子类也不能实例化

### 自定义类

类其实是一个类定义和各种方法的自由组合

实现方法：

* 定义类和函数,然后手动通过类赋值
* 借助MethodType实现
* 借助于type实现
* 利用元类MetaClass

```python
# 自己定义一个类
class A():
    pass
    def say(self):
        print("Sayihng......")

A.say = say
a = A()
a.say()

# 借助MethodType
from types import MethodType
class A():
    pass
    def say(self):
        print("Saying......")
a = A()
a.say = MethodType(say,A)
a.say()

# 借助type
def say(self):
    print("Saying.......")
def talk(self):
    print("Talking.......")
A = type("AName",(object,),{"class_say":say, "class_talk":talk})
a = A()
a.class_say()
a.class_talk()

# 借助MetaClass
class TulingMetaClass(type):
    def __new__(cls,name,bases,attrs):
        return type.__new__(cls,name,bases,attrs)
class Teacher(object,metaclass=TulingMetaClass):
    pass
t=Teacher()
```
