# Kubernetes

Kubernetes 提供了面向应用的容器集群部署和管理系统,最初起源于 Google 内部的 Borg 系统

## Kubernetes 架构

Kubernetes 借鉴了 Borg 的设计理念,整体架构于 Borg 非常像

![Borg 架构](./Pics/borg.png)
![Kubernetes架构](./Pics/kubernetes.png)

Kubernetes 有以下几个核心组件构成:

* etcd 保存整个集群的状态;
* APIserver 提供资源操作的唯一接口,并提供认证,授权,访问控制,API注册和发现等级制;
* controller manager 负责维护集群的状态,比如故障检测,自动拓展,滚动更新等;
* scheduler 负责资源的调度,按照云顶的调度策略将 Pod 调度到相应的机器上;
* kubelet 负责维护容器的声明周期,同时负责 Volume(CSI) 和网络(CNI)的管理;
* Container runtime 负责镜像管理以及 Pod 和容器的运行(CRI);
* kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡;

除了核心组件,还有一些推荐的插件:

* CoreDNS 负责为整个集群提供 DNS 服务;
* Ingress Controller 为服务提供外网入口;
* Prometheus 提供资源监控;
* Dashboard 提供 GUI
* Federation 负责跨可用区的集群

## Kubernetes 概念对象

### Pod

Pod 是 Kubernetes 中最基础的运行部署应用或服务的最小单元,可以是多容器的(支持在一个 Pod 的多个容器中共享网络地址和文件系统,通过进程间通信和文件共享完成服务)

### Replication Controller, RC

RC 是 Kubernetes 集群中保证 Pod 高可用的 API 对象,通过监控运行中的 Pod 来保证集权中运行指定数目的 Pod 副本

### Replica Set, RS

RS 是新一代 RC,提供同样的高可用能力,区别主要是 RS 能支持更多中种类的匹配模式,一般不单独使用,而是作为 Deployment 的理想状态参数使用

### Deployment

Deployment 表示用户对 Kubernetes 集群的一次更新操作,可以创建或更新一个新的服务,支持滚动升级一个服务(通过创建一个新服务,并增加副本数,将旧的 RS 副本减少到0)

### Service

稳定提供服务发现和均衡负载能力,每个 Service 对应一个集群内部有效的虚拟 IP,集群内部通过虚拟 IP 访问一个服务

### Job

Job 是 Kubernetes 用来控制批处理型任务的 API 对象,Job 管理的 Pod 根据用户的设置把任务成功完成就会自动退出

### DaemonSet

DaemonSet 的关注点在 Kubernetes 集群职工的节点,要保证每个节点都有一个此类 Pod 运行,典型的 DaemonSet 包括存储,日志和监控等

### StatefulSet

用于控制有状态服务,StatefulSet 中的每个 Pod 的名字都是事先确定的,不能更改;每个 StatefulSet 中的 Pod 挂载自己独立的存储,如果出现故障,启动一个新的 Pod 后要挂载原来的 Pod;典型服务包括数据库,集群化管理服务等有状态服务

### Federation

提供跨区域,跨服务商的集群服务;通过注册 Kubernetes Cluseter 实现负载均衡

### Volume

类似 Docker 的存储卷,但 Kubernetes 的卷的声明周期和作用范围是一个 Pod, 存储卷由 Pod 中的所有容器共享

### Persistent Volume, PV 和 Persistent Volume Claim, PVC

提供了存储的逻辑抽象,使得 Pod 在逻辑上可以忽略实际的存储技术;而 PV 提供资源, PVC 使用资源

### Node

实际提供计算能力,是所有 Pod 运行所在的工作主机,可以是物理机也可以是虚拟机

### Secret

用于保存和传递密码,密钥,认证凭据,避免把敏感数据写在明文中

### User Account 和 Service Account

User Account 为人提供账户标识, Service Account 为 Pod 提供账户标识;而 User Account 是跨 namespace 的,由于 Service Account 对应的是程序的身份,所以与特定 namespace 是相关的

### Namespace

为 Kubernetes Cluster 提供虚拟的隔离作用,初始有两个 namespace 分别是 default 和 kube-system

### RBAC 访问授权

Role-based Access Control 基于角色的访问控制,访问策略和角色关联,具体用户和一个或多个角色相关联

## Etcd 解析

Etcd 用于保存集群所有的网络配置和对象的状态信息
