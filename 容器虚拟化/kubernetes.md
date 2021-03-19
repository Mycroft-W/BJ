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

RC 是 Kubernetes 集群中保证 Pod 高可用的 API 对象,通过监控运行中的 Pod 来保证集权中运行指定数目的 Pod 副本;新版不建议使用

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

### Etcd 解析

Etcd 用于保存集群所有的网络配置和对象的状态信息

## K8s中的资源

|资源类型|具体资源|
|--|--|
|工作负载型,workload|Pod,ReplicaSet,Deployment,StatefulSet,DaemonSet,Job,CronJob|
|服务发现及负载均衡,ServiceDiscovery LoadBalance|Service,Ingress|
|配置与储存型|Volume,CSI|
|特殊类型的存储卷|ConfigMap,Secret,DownwardAPI|
|集群级资源|Namespace,Node,Role,ClusterRole,RoleBinding,ClusterRoleBinding|
|元数据|HPA,PodTemplate,LimitRange|

### 资源清单

资源清单是一个 yaml 文件,其中详细写明了资源的类型,所需的环境等信息,用于创建一个符合预期的 Pod;在使用时使用
kubectl 指定文件,kubectl 读取 yaml 文件后会将其序列化为 json 格式传递给 kubeapiserver 然后控制 kubelet 创建 pod

使用方式:

```shell
kubectl create -f <yaml文件>
```

资源清单的基本格式如下:

```yaml
apiVersion: group/apiversion    # 指定使用的apiversion
kind:                           # 资源类型
metadata:                       # 元数据
  name:                           # 资源名
  namespace:                      # 命名空间默认是 default
  lables:                         # 标签
  annotations:                    # 注解
spec:                           # 对资源期望的状态
status:                         # 最近状态,由 k8s 自动维护
```

每种资源的详细内容可使用以下命令查看:

```shell
kubectl api-versions            # 查看api-version
kubectl explain <资源>           # 查看资源文档
kubectl explain <资源.字段>      # 查看具体字段文档
```

Pod 资源清单示例:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-demo
  namespace: default
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-1
    image: harbor.hongfu.com/library/myapp:v1
  - name: busybox-1
    image: harbor.hongfu.com/library/busybox:v1
    command:
    - "/bin/sh"
    - "-c"
    - "sleep 3600"
```

## Pod 详解

Pod 是 Kubernetes 调度的最小单位, k8s 的大多服务以及应用都是运行在 Pod 中(kubelet 运行在主机中)

Pod 中的容器共享网络和存储,Pod 中的容器可以使用 localhost 互相通信,可以直接通过进程间通信

### Pod 的生存周期

一个 Pod 从创建删除一般经过以下几个阶段: 创建 pause 容器,init 初始化,创建应用容器(可以有多个,并行启动),删除容器;其中创建应用容器还可以有 PostStart 和 PerStop 阶段以及就绪探测和生存探测

* pause 容器: 用于共享网络栈,存储卷,生命周期与 Pod 等长
* init 初始化:在初始化阶段可先启动一些容器(initC)以生成应用容器所需要的资源
* PostStart: 在应用容器启动后进行动作
* PerStop: 在应用容器结束前进行动作
* 就绪探测: 在应用容器启动后,探测是否具备某些资源
* 生存探测: 在应用容器启动后,对其中的应用进行探测,伴随整个容器的生命周期

#### pause 容器

可以视为一个中间容器,首先会创建出 pause 容器,后面创建的应用容器通过加入 pause 容器的网络栈和分享存储卷,使得一个 Pod 中的容器有共同的网络栈和存储卷

#### Init 容器

通过在 spec 中使用`initContainers`字段,以标记容器为 initC

Init 容器为串行运行,前一个运行并成功退出后,才运行后一个

相比于应用容器,init 容器使用 Linux Namespace;因此能够访问 Secret

initC 示例:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:                     # 应用容器,当所有 init 容器成功退出后运行
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:                 # init 容器
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']                      # 检测myservice 服务,成功后退出
  - name: init-mydb
    image: busybox
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']
```

## 控制器

对资源进行操作,使资源达到预期;控制 Pod 的具体状态和行为;控制器通过匹配 labels 来进行判断控制那些 Pod

### Deployment 详解

提供了一个声明式定义(declarative)方法,对应用进行操作,使应用符合预期,Deployment 通过创建 ReplicaSet, ReplicaSet 再创建 Pod 的方式管理 Pod

Deployment 典型的应用场景有:

* 定义 Deployment 来创建 ReplicaSet 和 Pod
* 滚动更新和回滚应用
* 扩容和缩容
* 暂停和继续 Deployment

Deployment 的 yaml 文件格式如下:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3    # Pod 的副本数
  template:    # 嵌套了 Pod 的定义,少了apiVersion和kind
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

#### 创建 Deployment

可以通过以下命令创建一个 Deployment:

```shell
kubectl create -f example.yaml  --record  # 通过指定yaml 文件创建,--record 记录对该资源的更新
kubectl get deployment,replicaset,pod # 查看资源
```

Deployment 中的 ReplicaSet 的名称是 `<Deployment名>-<Pod模板hash值>`

#### 更新 Deployment

需要注意的是 Deployment 的 rollout 只有在 Deployment 的 pod template 中的 label 或镜像更新时被触发,其他更新,例如扩容并不会触发 rollout;Deployment 的更新方式是,删除旧的 Pod,创建新的 ReplicaSet 并新建 Pod,直到旧的 Pod 为零,,但 Deployment 会保留旧的 ReplicaSet 用于回滚

可以通过命令更新,或者修改yaml文件达到更新目的

```shell
kubectl set image deployment/nginx-deployment nginx=nginx:1.91    # 修改镜像
kubectl edit deployment/nginx-deployment      # 编辑资源在etcd中的信息
```

在更新后可以查看状态

```shell
kubectl rollout status deployment/niginx-deployment
```

Deployment 在更新时为了保证应用的可用,不会同时更新所有 Pod,而是按照一定比例来逐渐更新,直到全部更新

**Rollover**:在前一次更新还未完成时,就进行再次更新,会导致前次更新停止,并删除旧的 Pod,开始最近的更新

#### 回滚 Deployment

默认情况下, kubernetes 会保存前两次的 Deployment 的 rollout 历史记录,以便随时回滚

首先,检查 Deployment 的 revision:

```shell
kubectl rollout history deployment/nginx-deployment # 查看revision
kubectl rollout history deploymnet/nginx-deployment --revision=2 # 查看单个 revision 的详细信息
```

然后回滚:

```shell
kubectl roolout undo deployment/nginx-deployment --to-revision=2 # 回滚,--to-revision 指定回滚版本
```

**注意**:由于 kubernetes 只会记录触发 rollout 的操作,所以当手动进行扩容后回滚只有 Deployment 中的 Pod template 才会回滚

#### ReplicationController & ReplicaSet

### DaemonSet 详解

### StatefulSet 详解

### Job & CronJob

## 服务发现

kubernetes 为了实现**服务实例间的负载均衡和不同服务间的服务发现,创造了 Service 对象**,同时为了**从集群外部访问集群创建了 Ingress 对象**

### Service 详解

Kubernetes 中的 Pod 在每个生命周期中的 IP 地址不总是稳定可依赖的,所以如果一组 Pod (backend)为其他 Pod (frontend)提供服务,那么 frontend 该如何发现并连接到backend?

Service 定义了一种抽象: 一个 Pod 的逻辑分组,一种可以访问到它们的策略(微服务),这组 Pod 能够被 Service 访问到(通过 Label Selector 实现)

通过 yaml 问价定义 Service, 写法如下:

```yaml
kind: Service             # 资源类型
apiVersion: v1            # api 版本
metadata:
  name: my-service        # 名称
spec:
  selector:               # 选择标签
    app: MyApp
  ports:                  # 端口
    - protocol: TCP       # 协议类型
      port: 80            # 暴露端口
      targetPort: 9376    # 目标端口(backend 端口)
```

上述配置会创建一个名为 `my-service` 的 Service 对象,它会将请求代理到, 具有`app=MyApp` 并开放 TCP 9876 端口的 Pod

可以在 Service 中定义多个端口,需要注意的是使用多个端口时,必须给出所有端口的名称

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
    selector:
      app: MyApp
    ports:
      - name: http              # 端口名称
        protocol: TCP           # 协议
        port: 80                # 端口
        targetPort: 9376        # 目标端口
      - name: https             # 端口名称
        protocol: TCP
        port: 443
        targetPort: 9377
```

#### Service 类型

在资源清单中通过`spec.type`字段指定一个需要的类型的 Service, 默认是 `ClusterIP`

* ClusterIP: 通过集群内部 IP 暴露服务,仅在集群内部可以访问
* NodePort: 通过每个 Node 上的 IP 和静态端口( NodePort) 暴露服务, 通过 `<NodeIp>:<NodePort>`,可以从集群外部访问服务
* LoadBalancer: 使用云提供商的负载均衡器,向外部暴露服务
* ExternalName: 通过返回 `CNAME`,将服务映射到`ExternalName`字段内容

##### NodePort 类型

kubernetes master 会从给定的配置范围内(默认:30000-32767)分配端口,每个 Node 将从该端口代理到 `Service`

##### LoadBalancer 类型

使用支持外部负载均衡器的云提供商的服务,为`Service`提供负载均衡器

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376              # backend 端口
      nodePort: 30061               # Node 端口
  clusterIP: 10.0.171.239
  loadBalancerIP: 78.11.24.19       # 负载均衡器的IP
  type: LoadBalancer                # Service 类型
status:
  loadBalancer:
    ingress:
      - ip: 146.148.47.155
```

来自外部负载均衡器的流量将直接负载到 `backend pod`上,实际工作过程,依赖于云提供商

##### ExternalName 类型

ExternalName Service 是 Service 的特例,他没有 selector,也没有定义任何的端口和 Endpoint, 通过返回该**外部服务**的别名来提供服务

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com       # 别名
```

#### Service 代理模式

在 Kubernetes 集群中,每个 Node 运行一个 kube-proxy 进程;kube-proxy 为 Service 实现了一种 VIP(虚拟IP)的形式

在 V1.0 版本,代理在 userspace; Service 是"四层"(TCP/UDP over IP) 概念

在 v1.1 版,新增了 iptables 代理;并新增了 Ingress API,用于表示"七层"(HTTP) 服务

从 v1.2 起,默认是 iptables 代理

在 v1.8.0 中,添加了 ipvs 代理;从 v1.14 默认使用,如果kube-proxy 检测到内核没有 ip_vs 模块,则会使用 iptables 代理模式

##### usersapce 代理模式

kube-proxy 会监控 Service 对象,对每个 Service,在本地 Node 打开一个端口,通过添加 iptables 规则捕获对 Service 的 clusterIP 的访问,然后将对代理端口的访问代理到 backend Pods 上

![userspace](./Pics/services-userspace-overview.jpg)

##### iptables 代理模式

kube-proxy 会监控 Service 对象,然后添加 iptables 规则捕获请求,利用 netfilter 进行重定向

![iptables](./Pics/services-iptables-overview.jpg)

##### ipvs 代理模式

kube-porxy 会监控 Service 对象,调用 netlink 接口创建 ipvs 规则,将流量重定向到一个后端 Pod

ipvs 相比 iptables, 同样基于 netfilter 的 hook 功能,但使用 hash 表作为底层数据结构并在内核空间中中作,因此性能更强;此外 ipvs 提供了更多的负载均衡算法

![ipvs](./Pics/service-ipvs-overview.png)

### Ingress 详解

通常情况下 Service 和 Pod 仅可在集群内部通过 IP 访问;而 Ingress 是授权入站连接到达集群服务的规则集合

**注意**: 为了使 Ingress 能正常工作,集群中必须运行 Ingress controller,而 kubernetes 集群自身并不含有,所以需要选择适合自己集群的 Ingress controller 或自己实现一个

* kubernetes 当前支持并维护 GCE 和 nginx 两种
* F5 支持维护 F5 BIG-IP Controller for Kubernetes
* Traefik 是功能齐全的 Ingress controller
* Istio 使用 CRD Gateway 来控制 Ingress 流量
