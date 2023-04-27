# MySQL备份

## 主从备份

1. 修改主库配置文件`/etc/my.cnf`，添加以下内容；修改配置文件后需要重启MySQL实例

    ```cnf
    [mysqld]
    log-bin=mysql-bin #指定binlog文件名称
    server-id=1 # serverid 主从不能相同
    binglog_do_db=test # 指定要同步的库，不指定则为所有库
    binlog_ignore_db=test
    ```

    从库只需要添加

    ```cnf
    server-id=2
    ```

2. 在Master创建从库同步用户，并赋予权限

    从库需要使用此用户链接主库，并从主库拉取binlog日志，从而达到同步的目的

    ```sql
    > CREATE USER 'slave'@'%' IDENTIFIED BY 'slave'；
    > GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' WITH GRANT OPTION;
    > FLUSH PRIVILEGES;
    ```

3. 查看master当前状态，并记录下binlog当前position

    ```sql
    > SHOW MASTER STATUS;
    +------------------+----------+--------------+------------------+-------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +------------------+----------+--------------+------------------+-------------------+
    | mysql-bin.000001 |     3911 | test         |                  |                   |
    +------------------+----------+--------------+------------------+-------------------+
    1 row in set (0.00 sec)
    ```

4. 在从库配置主库的信息

    ```sql
    > CHANGE MASTER TO MASTER_HOST='master_ip',MASTER_USER='slave',MASTER_PASSWORD='slave',MASTER_LOG_FILE='mysql-bin.000001',MASTER_LOG_POS=3911;

    CHANGE MASTER TO MASTER_HOST='192.168.30.192',MASTER_USER='slave',MASTER_PASSWORD='Slave@2021',MASTER_LOG_FILE='mysql-bin.000025',MASTER_LOG_POS=38496880;
    ```

5. 查看从库状态

    ```sql
    > SHOW SLAVE STATUS\G;

    *************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.2.45
                  Master_User: slave
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000002
          Read_Master_Log_Pos: 6793169
               Relay_Log_File: zbsy-MS-7D20-relay-bin.000002
                Relay_Log_Pos: 5526901
        Relay_Master_Log_File: mysql-bin.000002
             Slave_IO_Running: Yes                                      # 看到这两个yes 表示从库配置成功
            Slave_SQL_Running: Yes
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
    Replicate_Wild_Ignore_Table: 
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 6793169
              Relay_Log_Space: 5527115
              Until_Condition: None
    ......
    ```

> **注意：** 在做主从备份的配置时要注意，要同步的库需要数据一致，如果是新库，则按照以上步骤执行即可；如果是有数据的库需要先将主库停下，复制已有数据到从库，然后按照以上步骤执行

## 定时全量备份

mysql提供了 `mysqldump`命令导出数据库，利用此命令配合shell脚本可以做到定时备份数据库

1. 编写备份 `mysqlbackup.sh` 脚本

    编写合适的脚本，并放入 `/home/user/` 路径下

    ```bash
    #!/usr/bin/bash

    NUMBER=15                               # 要保留的备份数量
    BACKUP_DIR=/home/user/mysqlbackup       # 备份文件位置
    DD=`date +%Y%m%d_%H`                    # 备份文件时间戳后缀
    USERNAME=user                           # 数据库用户名
    PASSWORD=password                       # 数据库密码
    DATABASE=backup_test                    # 要备份的库名

    # 判断如果不存在备份文件夹则创建
    if [ ! -d $BACKUP_DIR ];then
        mkdir -p $BACKUP_DIR
    fi

    # 备份命令
    mysqldump -u$USERNAME -p$PASSWORD $DATABASE > $BACKUP_DIR/${DATABASE}_$DD.sql

    # 删除早于15天的备份
    if [ `ls | wc -l` -gt $NUMBER ];then
        find $BACKUP_DIR -name "${DATABASE}_*.sql" -ctime +$NUMBER -exec rm {} \;
    fi
    ```

2. 编写 `mysqlbackup.service` 文件

   编写用于配合定时任务的 service 文件，并放入 `/usr/lib/systemd/system` 路径下

   ```service
    [Unit]
    Description=Mysql backup service

    [Service]
    Type=simple
    ExecStart=/usr/bin/bash /home/zbsy/mysqlbackup.sh   # 指定备份任务的运行命令
   ```

3. 编写 `mysqlbackup.timer` 文件

    编写 systemd 的定时任务文件，并放入 `/usr/lib/systemd/system` 路径下

    ```service
    [Unit]
    Description=Run mysqlbackup service

    [Timer]
    OnCalendar=*-*-* 02:00:00           # 在每天的02时启动一次备份任务
    Unit=mysqlbackup.service            # 备份任务的 service 文件

    [Install]
    WantedBy=multi-user.target
    ```

4. 测试服务

   在完成服务的编写后，执行 `systemctl start mysqlbackup.service` 命令，查看是否有备份文件产生

5. 配置定时任务开机自动启动

    使用 `systemctl enable mysqlbackup.timer` 命令，配置定时任务开机自启
