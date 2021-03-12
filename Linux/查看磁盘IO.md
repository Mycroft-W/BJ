# 查看磁盘IO

可以使用`iostat`命令, 可以显示基础的系统信息,cpu平均使用率;最重要的就是会显示所有磁盘的IO使用情况

![DiskIO](./Pics/DiskIO.png)

如果要更具体的,某个进程的磁盘IO信息,可以使用`pidstat -d`查看

默认展示当前一秒的IO使用,如果要一段时间的统计可以使用`pidstat -d 1 10`,每秒刷新一次,统计十次也就是10s内的使用,结束时显示平均值

![pidstat](./Pics/pidstat.png)
