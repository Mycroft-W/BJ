'''
for i in range(1, 10):
    for j in range(1, i + 1):
        print(i * j, end=" ") # 以空格结束
    print() # print（）默认以换行结束
'''

'''
# 函数形式
def nine_nine():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(i * j, end=" ")  # 以空格结束
        print()  # print（）默认以换行结束
    return None


nine_nine()

'''


# 改造上面的函数
def printLine(line_num):
    '''
    line_num:代表行号

    打印一行九九乘法表
    '''
    for i in range(1, line_num + 1):
        print(line_num * i, end=" ")
    print()
    return None


def nineNine():
    for i in range(1, 10):
        printLine(i)

    return None


nineNine()
