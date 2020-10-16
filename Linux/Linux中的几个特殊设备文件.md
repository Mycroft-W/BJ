# Linux中的几个特殊字符设备文件

## /dev/full

是一个始终充满的设备，在写入时总是返回”No space left on device“

## /dev/random

阻塞式随机源，收集系统熵以生成随机数，在熵用完后阻塞

## /dev/urandom

非阻塞式随机源，不断产生随机数，不会阻塞

## /dev/null

丢弃一切重定向到此设备的数据，被称为位桶（bit bucket）或黑洞（black hole）

~~~shell
# 例子
lspci > /dev/null # 将lspci的结果丢弃，不会返回任何结果
~~~

## /dev/zero

不断产生 null （空字符，二进制0的数据流），通常用于清除文件内容或者初始化存储设备

~~~shell
# 例子
dd if=/dev/zero of=/dev/sda # 清除 sda 上的数据

dd if=/dev/zero of=foobar count=1024 bs=1024 # 创建一个1M的文件叫 foobar；count 块数量；bs 块大小
~~~

