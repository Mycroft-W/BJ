# Firebird 数据库备份

Firebird 本身自带了备份工具， gbak, nbackup, fbsvcmgr, 其中：

* gbak 支持备份远程主机数据库到本地，但不支持增量备份
* nbackup 支持增量备份，但只能在本地备份，无法远程调用
* fbsvcmgr 这个命令更像是远程管理工具，支持远程调用 nbackup ，但同样的无法将远程数据库备份到本地

gbak 命令使用

```bat
gbak.exe -b 192.168.1.2:D:\Firebird\test.fdb D:\backup\test.fbk -user sysdba -password masterkey
// 以上命令是将192.168.1.2的test.fdb 库备份到了本地的test.fbk

gbak.exe -r D:\backup\test.fbk 192.168.1.2:D:\Firebird\test.fdb -user sysdba -password masterkey
// 以上命令是将备份恢复到远程服务器上

```

fbsvcmgr 命令使用

```bat
fbsvcmgr 192.168.1.2:service_mgr -user sysdba -password masterkey -action_nbak -nbk_level 0 -dbname D:\Firebird\test.fdb -nbk_file D:\backup\test.nbk

// 以上命令是控制远程服务器使用nbackup命令在服务器本地进行增量备份
```

通过编写脚本（windows 下为bat脚本）配合定时任务，可以实现自动备份任务

bat 脚本内容如下

```bat
# 定义 Ymd 为当前时间，
set "Ymd=%date:~,4%%date:~5,2%%date:~8,2%"
# 定义 obj_dir 为备份文件的位置
set "obj_dir= D:\databases_firebird\"
# 创建文件夹
md %obj_dir%
# 使用firebird自带的gbak命令，进行备份； -b为要备份库的位置 -user 库用户名，-password 库密码
"D:\Firebird\Firebird_2_5\bin\gbak.exe" -b localhost:D:\databases_firebird\test.fdb D:\backup\test_%Ymd%.fbk -user sysdba -password masterkey
# 查找目录中早于15天的文件并删除
forfiles /p "D:\backup" /s /m *.fbk /d -15 /c "cmd /c del @path"
exit
```
