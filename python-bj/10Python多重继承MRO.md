# MRO（method resolution order）从python2.3之后使用C3算法,之前是使用深度优先算法。用于在多继承时判断调用的属性的路径（来自哪个类）

C3算法最早被提出是用于Lisp的,应用在Python中是为了解决基于深度优先搜索算法不满足本地优先级,和单调性的问题。

本地优先级：指声明时父类的顺序,比如C(A,B),如果访问C类对象属性时,应该根据声明顺序,优先查找A类,然后再查找B类。

单调性：如果在C的解析顺序中,A排在B的前面,那么在C的所有子类里,也必须满足这个顺序。  
**C3算法**

判断mro要先确定一个线性序列,然后查找路径由由序列中类的顺序决定。所以C3算法就是生成一个线性序列。

如果继承至一个基类:

class B(A)

这时B的mro序列为[B,A]

如果继承至多个基类

class B(A1,A2,A3 ...)

这时B的mro序列 mro(B) = [B] + merge(mro(A1), mro(A2), mro(A3) ..., [A1,A2,A3])

**merge操作就是C3算法的核心。**

 遍历执行merge操作的序列,如果一个序列的第一个元素,在其他序列中也是第一个元素,或不在其他序列出现,则从所有执行merge操作序列中删除这个元素,合并到当前的mro中。

merge操作后的序列,继续执行merge操作,直到merge操作的序列为空。

如果merge操作的序列无法为空,则说明不合法。

例子：

class A(O):pass

class B(O):pass

class C(O):pass

class E(A,B):pass

class F(B,C):pass

class G(E,F):pass

A,B,C都继承至一个基类,所以mro序列依次为[A,O],[B,O],[C,O]

mro(E) = [E] + merge(mro(A), mro(B), [A,B])

   = [E] + merge([A,O], [B,O], [A,B])

执行merge操作的序列为[A,O],[B,O],[A,B]

A是序列[A,O]中的第一个元素,在序列[B,O]中不出现,在序列[A,B]中也是第一个元素,所以从执行merge操作的序列([A,O],[B,O],[A,B])中删除A,合并到当前mro,[E]中。

mro(E) = [E,A] + merge([O], [B,O], [B])

再执行merge操作,O是序列[O]中的第一个元素,但O在序列[B,O]中出现并且不是其中第一个元素。继续查看[B,O]的第一个元素B,B满足条件,所以从执行merge操作的序列中删除B,合并到[E, A]中。

mro(E) = [E,A,B] + merge([O], [O])

   = [E,A,B,O]

同理

mro(F) = [F] + merge(mro(B), mro(C), [B,C])

​     = [F] + merge([B,O], [C,O], [B,C])

​     = [F,B] + merge([O], [C,O], [C])

​     = [F,B,C] + merge([O], [O])

​     = [F,B,C,O]

mro(G) = [G] + merge(mro[E], mro[F], [E,F])

​     = [G] + merge([E,A,B,O], [F,B,C,O], [E,F])

​     = [G,E] + merge([A,B,O], [F,B,C,O], [F])

​     = [G,E,A] + merge([B,O], [F,B,C,O], [F])

​     = [G,E,A,F] + merge([B,O], [B,C,O])

​     = [G,E,A,F,B] + merge([O], [C,O])

​     = [G,E,A,F,B,C] + merge([O], [O])

​     = [G,E,A,F,B,C,O]
