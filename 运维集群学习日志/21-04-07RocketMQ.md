# RocketMQ

RocketMQ 是一个分布式消息中间件,主要有四个构成部分, NameServer, Broker, Producer, Consumer

![RocketMQ-arch](./Pics/rmq-basic-arc.png)

* NameServer, 提供了一个轻量级服务发现和路由控制
* Broker, 负责消息存储并提供了轻量级的*主题*和*队列*机制; 支持*Push*和*Pull*模式,提供了容错机制
* Producer, 作为消息的生产者会将消息发送给 Broker 存储
* Consumer, 是消息的消费者可以部署为*Push*或*Pull*模式,同样支持*集群*和*广播*方式;提供了实时的订阅机制

## NameServer

NameServer 包括了两个特性:

* Broker 管理,NameServer 负责 Broker 注册并提供了 hearbeat 机制来检查 Broker 的可用性
* 路由管理,每一个 NameServer 都存储了完整的路由信息和队列信息

## Broker Server

Broker 提供了消息存储,转发和验证,以及高可用保障等;Broker 有以下模块来实现上述功能:

* Remoting Module, 是 broker 的入口,处理客户端请求
* Client Manager, 管理客户端(Producer/Consumer)并维护消费者的主题订阅
* Store Service, 提供简单 API 用于在磁盘上存储查询消息
* HA Service, 提供了 master 和 slave 之间的数据同步功能
* Index Service, 依靠特殊的键来建立消息索引用于消息的快速查询

## 部署方式

在启动 RockerMQ 集群时,一定要先启动 NameServer 然后启动 Broker

```shell
nohup sh mqnamesrv &
# 启动 nameserver

nohup sh mqbroker -n 192.168.1.1:9876 -c $ROCKETMQ_HOME/conf/1m-noslave/broker-a.properties &
# 启动 Broker Master; -n 指定 nameserver 地址,多个用分号隔开

nohup sh mqbroker -n 192.168.1.1:9876 -c $ROCKETMQ_HOME/conf/1m-noslave/broker-a-s.properties &
# 启动 Broker Slave
```

RocketMQ 有以下几种部署方式,不同的部署方式各有优劣:

### 单 Master 模式

这种方式风险较大,一旦Broker重启或者宕机时,会导致整个服务不可用.不建议线上环境使用,可以用于本地测试

### 多 Master 模式

一个集群无Slave,全是Master,例如2个Master或者3个Master,这种模式的优缺点如下:

优点:配置简单,单个Master宕机或重启维护对应用无影响,在磁盘配置为RAID10时,即使机器宕机不可恢复情况下,由于RAID10磁盘非常可靠,消息也不会丢(异步刷盘丢失少量消息,同步刷盘一条不丢),性能最高;

缺点:单台机器宕机期间,这台机器上未被消费的消息在机器恢复之前不可订阅,消息实时性会受到影响

### 多 Master 多 Slave 模式-异步复制

每个Master配置一个Slave,有多对Master-Slave,HA采用异步复制方式,主备有短暂消息延迟（毫秒级）,这种模式的优缺点如下:

优点:即使磁盘损坏,消息丢失的非常少,且消息实时性不会受影响,同时Master宕机后,消费者仍然可以从Slave消费,而且此过程对应用透明,不需要人工干预,性能同多Master模式几乎一样;

缺点:Master宕机,磁盘损坏情况下会丢失少量消息

### 多 Master 多 Slave 模式-同步复制

每个Master配置一个Slave,有多对Master-Slave,HA采用同步双写方式,即只有主备都写成功,才向应用返回成功,这种模式的优缺点如下:

优点:数据与服务都无单点故障,Master宕机情况下,消息无延迟,服务可用性与数据可用性都非常高;

缺点:性能比异步复制模式略低（大约低10%左右）,发送单个消息的RT会略高,且目前版本在主节点宕机后,备机不能自动切换为主机

**注**: Master 和 Slave 是通过相同的 BrokerName 参数来配对的,Master 的 BrokerId 必须为0, Slave 的 BrokerId 是大于零的整数

## RocketMQ 性能调优

1. OS 优化
   1. 最大文件数量`/etc/security/limits.conf`

      ```conf
      # <domain> <type> <item> <value>
      baseuser soft nofile 655360
      baseuser hard nofile 655360
      * soft nofile 655360
      * hard nofile 655360
      ```

   2. 内核参数`/etc/sysctl.conf`

      ```conf
      vm.overcommit_memory=1
      # 内存超分
      # 0, 申请时检查
      # 1, 申请就分配,直到占满
      # 2, 禁止超分

      vm.drop_caches=1
      # 写入时,清空缓存,相当于 sync
      # 1, 清空页缓存
      # 2, 清空 inode 和目录树
      # 3, 都清空

      vm.zone_reclaim_mode=0
      # 0, 倾向从其他节点分配内存
      # 1, 倾向从本地节点回收 cache 内存

      vm.max_map_count=655360
      # 进程最大能拥有的内存区域,默认 65536

      vm.dirty_background_ratio=50
      # 当 dirty cache 到达多少时,启动 pdflush 进程,将 dirty cache 写回磁盘

      vm.dirty_ratio=50
      # 当一个进程的 dirty cache 到了多少的时候,启动 pdflush 进程,将 dirty cache 写回磁盘

      vm.dirty_writeback_centisecs=360000
      # pdflush 每隔多久,自动运行一次

      vm.page-cluster=3
      # swap 操作多少内存页(2的指数)

      vm.swappiness=1
      # 0, 仅在内存不足的情况下,当剩余空闲内存低于 vm.min_free_kbytes limit 时,
      ```

2. JVM 优化

   ```shell
   -server -Xms8g -Xmx8g -Xmn4g
   # 调整堆大小

   -XX:+AlwaysPreTouch
   # 预分配页面,应响启动速度

   -XX:-UseBiasedLocking
   # 禁用偏置锁,减少 JVM 停顿

   -XX:+UseG1G -XX:G1HeapRegionSize=16m -XX:G1ReservePercent=25 -XX:InitiatingHeapOccupancyPercent=30
   # 使用 G1 垃圾回收

   -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=5 -XX:GCLogFileSize=30m
   # GC 滚动日志

   -Xloggc:/dev/shm/mq_gc_%p.log
   # 将 GC 日志重定向到文件系统
   ```

3. RocketMQ 优化

   ```conf
   flushDiskType=ASYNC_FLUSH        # 异步刷盘

   transientStorePoolEnable=true    # 开启对外内存

   warmMapedFileEnable=true         # 开启文件预热

   slaveReadEnable=true             # slave 读权限

   transferMsgByHeap=false          # 关闭堆内存数据传输
   ```
