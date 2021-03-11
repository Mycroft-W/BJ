# 容器技术

On-Premises,本地部署
IaaS(Infrastructure as a Service),基础设施即服务
PasS(Platform as a Service),平台即服务
SaaS(Software as a Service),软件即服务

更轻量级的虚拟化技术,基于 Linux 的内核功能(namespace, cgroup),在Linux 中早期出现的LXC,后出现的 docker 基于lxc并进行一系列改进添加了基于Overlay 类的Union FS等技术,后经过多次技术迭代后成为了现在应用最广泛的容器技术

![Containers vs VMs](Pics\VMvsContainers.png)
![docker特性](Pics\dockervscontainer.png)

## docker 简介

docker 是C/S架构的软件,由docker client 和 docker server 构成;docker 使用分层复用的方式减轻镜像的容量

docker 三要素: 容器(container),镜像(image),仓库(repository)

* 镜像: 封装完成的服务及运行所需环境,利用Union FS的技术,分层构建

* 容器: 镜像运行的实例,实质是进程,但拥有自己独立的命名空间

* 仓库: 存储镜像的仓库,其中的镜像通过\<仓库名>:\<标签> 来表示镜像

## docker 加速配置

由于docker 的官方仓库位于国外,直接访问速度很慢,通过配置加速器来提升镜像的获取速度
国内主要有 阿里云, 网易云, 道云等,具体网址到各官网查看;配置方法: 将 --registry-mirror 加入到 Docker 配置文件 /etc/docker/daemon.json 中

在配置完成后,重启docker 的守护进程;然后可以使用命令查看

```bash
docker info
```

## docker 基础命令

格式: docker 命令关键字 参数

### 镜像管理

|命令|描述|
|--|--|
|docker pull|拉取镜像,默认从官方仓库|
|docker image ls/ docker images|列出本地镜像|
|docker system df|统计镜像真实容量|
|docker image ls -f dangling=true|显示虚悬镜像|
|docker image prune|删除无用镜像,默认虚悬镜像|
|docker image rm|删除本地镜像|

**虚悬镜像**: 由于新旧镜像同名,旧镜像名称被取消,从而出现仓库名,标签均为\<none>的镜像

**中间层镜像**: 在构建镜像时会利用中间层镜像加速构建,被上层镜像依赖

由于镜像的依赖,当镜像的依赖为零时,才会删除该镜像

## 定制镜像

使用Dockerfile 定制镜像,以一个镜像为基础,在其上进行定制;Dockerfile 中写的是对每一层修改,安装,构建,操作的命令

FROM 命令指定基础镜像:

```dockerfile
FROM nginx
RUN echo '<h1> Hello,Docker!</h1>' > /usr/share/nginx/html/index.html
```

Docker 存在一个特殊镜像,"scratch"; 这个镜像是虚拟的概念,并不实际存在,它表示一个空白镜像

### 构建镜像

使用以下命令进行构建:

```bash
docker build [options] <context_path/URL>
```

docker build 还支持从URL构建,也可以用给定的tar压缩包构建,还可以从标准输入中读取Dockerfile进行构建

### Dockerfile 指令

|指令|描述|
|--|--|
|FROM|指定基础镜像|
|RUN|运行指定命令|
|COPY|复制文件|
|ADD|更高级的文件复制,推荐仅在需要自动解压的场合使用|
|CMD|容器启动默认命令|
|ENTRYPOINT|入口点|
|ENV|设置环境变量|
|ARG|构建参数|
|VOLUME|定义匿名卷|
|EXPOSE|暴露端口|
|WORKDIR|指定工作目录|
|USER|指定当前用户|
|HEALTHCHECK|健康检查|
|ONBUILD|在当前镜像被作为基础镜像时,执行命令|
|LABEL|添加元数据|
|SHELL|指定RUN,ENTRYPOIN,CMD命令的shell|

#### RUN 运行

RUN 命令有两种方式:

```dockerfile
RUN <命令>                              # shell 格式
RUN ["可执行文件", "参数1", " 参数2"]    # exec 格式
```

每一个RUN行为,会新建一层;而 Union FS 有最大层限制,Overlay 最大128层;需要执行多条命令时要使用`&&`连接,镜像存储时每一层的东西并不会在下一层被删除,所以在每层构建后要清理掉无关文件

#### COPY 复制

COPY 命令有两种方式:

```dockerfile
COPY [--chown=<user>:<group>] <src> <dist>
COPY [--chown=<user>:<group>] ["<src>","<dist>"]
```

源路径为构建上下文的目录中的相对路径,目标路径可以时容器内的绝对路径,也可以是相对于工作目录的行对路径;使用COPY命令,文件的元数据会保留

#### ADD 复制

ADD 功能与COPY 基本一致,但增加了功能,源路径可以是URL,docker 会下载路径文件,权限为600;源路径也可以是一个 tar压缩文件,ADD命令会自动解压缩文件到目标路径

#### CMD 容器命令

CMD 有两种形式:

```dockerfile
CMD <命令>                                 # shell 格式
CMD ["可执行文件", "参数1", "参数2"...]     # exec 格式
```

shell 格式的命令,在实际执行中会被封装成以下格式:

```dockerfile
CMD ["sh", "-c", "命令"]
````

docker 中的应用应该都以前台执行,docker 要求至少有一个前台应用,否则会直接销毁容器;正确的启动服务方式应该是直接使用命令,并以前台形式启动

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

#### ENTRYPOINT 命令入口

ENTRYPOINT 有两种形式:

```dockerfile
ENTRYPOINT <命令>                              # shell 格式
ENTRYPOINT ["可执行文件", "参数1", "参数2"...]  # exec 格式
```

在指定 ENTRYPOINT 后, CMD 的内容不会直接执行,而是会被作为参数传递给ENTRYPOINT 命令;在运行容器时可以使用`--entrypoint`来指定

```dockerfile
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["redis-server"]

# 以上两条命令会变成
ENTRYPOINT ["docker-entrypoint.sh" "redis-server"]
```

#### ENV 环境变量

ENV 有两种格式:

```dockerfile
ENV <key> <value>
ENV <key1>=<value1> <key2>=<value2>...
```

其他命令可以直接使用ENV中定义的环境变量

#### ARG 环境变量

ARG 格式:

```dockerfile
ARG <参数名>[=<默认值>]
```

ARG设置的环境变量在容器运行时不会保存,但使用 `docker history` 能看到;构建时可以使用`--build-arg <参数名>=<值>`来覆盖

ARG 命令有生效范围,在FROM之前定义的就只能用于FROM中

#### VOLUME 匿名卷

VOLUME 格式:

```dockerfile
VOLUME ["<路径1>", "<路径2>"...]
VOLUME <路径>
```

容器运行时应尽量保持容器存储层不发生写操作,在运行时将某些目录挂载为匿名卷;使用`-v 卷名:路径`可以替代匿名卷的挂载

#### EXPOSE 暴露端口

EXPOSE 格式:

```dockerfile
EXPOSE <端口1> [<端口2>...]
```

声明使用端口,但不会开启端口服务,在运行时使用`-P`随机映射时会自动映射到EXPOSE的端口

#### WORKDIR 工作目录

WORKDIR 格式:

```dockerfile
WORKDIR <路径>
```

相对路径的基准;如果没有则会新建

#### USER 当前用户

USER 格式:

```dockerfile
USER <用户名>[:<用户组>]
```

改变当前用户;不会新建用户,只能指定存在的

#### HEALTHCHECK 健康检查

HEALTHCHECK 格式:

```dockerfile
HEALTHCHECK [选项] CMD <命令>           # 设置检查容器健康的命令
HEALTHCHECK NONE                       # 如果基础镜像有检查指令,屏蔽掉
```

支持以下选项:

`--interval=<间隔>`: 检查间隔,默认30s

`--timeout=<时长>`: 超时时间,超过则认为健康检查失败,默认30s

`--retries=<次数>`: 失败次数,默认3次

CMD,ENTRYPOINT,HEALTHCHECK只可以出现一次,出现多个,只有最后一个生效

#### ONBUILD 被动执行

ONBUILD 格式:

```dockerfile
ONBUILD <其他指令>
```

在ONBUILD 后的指令,只有在本镜像被作为基础镜像时执行

#### LABEL 标签

LABEL 格式:

```dockerfile
LABEL <key1>=<value1> <key2>=<value2>...
```

给镜像添加一些元数据,作者,邮件等等信息

#### SHELL 指定shell

SHELL 格式:

```dockerfile
SHELL ["可执行文件", "参数"]
```

用于指定 RUN,ENTRYPOINT,CMD 的shell; Linux 中默认为 ["/bin/sh", "-c"]

### Dockerfile 多阶段构建

在Docker 17.05版本后引入的新功能,在之前是通过将完整的构建过程分散到多个Dockerfile 来实现类似效果

多阶段构建能够有效的减少镜像的体积,基本原理就是将构建编译环境的过程**开发环境**和构建程序的**生产环境**过程分为多个阶段,在最后阶段复制前阶段的生成结果,可以在最后的镜像中不包含编译器,依赖库等文件;最终镜像是以最后的FROM 作为基础镜像的

```dockerfile
FROM golang:1.9-alpine as builder       # 为阶段起别名
RUN apk --no-cache add git
WORKDIR /go/src/github.com/go/helloworld/
RUN go get -d -v github.com/go-sql-driver/mysql
COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
FROM alpine:latest as prod
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/go/helloworld/app .
CMD ["./app"]
```

## 镜像的实现原理

Docker 使用 Union FS 将不同的层结合到一个镜像中;通常Union FS 有两个用途,一方面可以实现不借助LVM,RAID将多个disk挂到同一个目录下,另一个更常用的就是将一个只读的分支和一个可写的分支联合在一起;Docker在OverlayFS上构建容器也是利用了类似的原理

## 容器操作

容器是镜像运行的实例,其中包含了运行的应用,以及运行态环境

### 容器管理

|命令|描述|
|--|--|
|docker run|基于镜像新建容器并启动|
|docker container start/stop|启动或停止已存在的容器|
|docker attach/exec|进入容器|
|docker export/import|导出/导入容器快照|
|docker container rm|删除终止态容器|
|docker container prune|清理所有终止态容器|

容器创建容器时,docker 会运行以下操作:

1. 检查本地是否有指定镜像,不存在则从共有仓库下载
2. 利用镜像创建并启动容器
3. 分配文件系统,并在只读的镜像层外面挂载一层可读写层
4. 从宿主机配置的网桥接口桥接一个虚拟接口到容器中
5. 从地址池分配一个ip地址给容器
6. 执行用户指定的应用程序
7. 执行完毕后终止容器

## 访问仓库

### docker hub

docker 官方维护了一个公共仓库 docker hub,通过执行`docker login` 可以登录docker hub

|命令|描述|
|--|--|
|docker search|搜索镜像|
|docker pull|拉取镜像|
|docker push|推送镜像|
|docker tag|给镜像打标签|

### 私有仓库

可以通过使用 docker-registry, nexus, harbor等工具构建私有镜像仓库

## docker 数据管理

在容器中管理数据主要有两种方式:

* 数据卷(Volumes)
* 挂载主机目录(Bind mounts)

### 数据卷

数据卷是一个可供一个或多个容器使用的特殊目录,有多种特性:

* 数据卷可以在容器之间共享和重用
* 对数据卷的修改立即生效
* 对数据卷的更新,不会影响镜像
* 数据卷默认会持续存在,删除容器无影响

|命令|描述|
|--|--|
|docker volume create \<name>|创建数据卷|
|docker volume ls|查看所有数据卷|
|docker volume rm \<name>|删除数据卷|
|docker volume prune|清理无主数据卷|

### 挂载主机目录

使用`--mount` 可以指定挂载一个本机目录或文件到容器,本机目录的路径必须是绝对路径,默认挂载属性为读写,可以指定为只读(readonly)

## docker 网络

docker 允许通过外部访问容器或容器互联的方式提供网络服务;在通常情况下,docker使用网桥`docker0`(bridge)与NAT的通信模式

### 外部访问容器

在运行容器时,可以通过`-P`和`-p`参数来指定端口映射,有三种格式对应三种情况:

* 映射所有接口地址 -- `hostPort:containerPort`
* 映射到指定地址的指定端口 -- `ip:hostPort:containerPort`
* 映射到指定地址的任意端口 -- `ip::containerPort`

### 容器互联

可以使用`--link`来连接容器,但更推荐将容器加入自定义的docker网络,在运行时通过`--network`来加入到网络

|命令|描述|
|--|--|
|docker network create|创建docker网络|
|docker network ls|查看存在的网络|
|docker network connect|将容器加入到网络|
|docker network rm|删除|

docker可以创建三种网络:

* bridge: 网桥模式
* none: 容器没有网络栈
* container: 使用其它容器的网络栈
* host: 表示容器使用host的网络,没有自己独立的网络栈;容器可以完全访问host 的网络,不安全

## Docker Compose

compose 是docker官方的开源项目,负责对docker容器集群的快速编排,它允许用户通过一个单独的`docker-compose.yml`模板文件来定义一组关联的应用容器为一个项目

docker compose 命令格式:

|命令|描述|
|--|--|
|docker-compose up|创建容器并启动;-f 指定yaml文件位置;-d 后台运行|
|docker-compose ps|显示所有容器|
|docker-compse pause|暂停容器|
|docker-compse restart|重启容器|
|docker-compse unpause|恢复暂停|
|docker-compse logs|查看日志|
|docker-compse rm|删除容器|
|docker-compse config -q|验证yaml配置是否正确|
|docker-compse stop|停止容器|
|docker-compse start|启动容器|

## docker 底层实现

docker 底层的核心技术包括Linux上的命名空间(Namespaces),控制组(Control groups),Union文件系统(Union file systems)和容器格式(Container format)

其中利用命名空间来做权限的隔离控制,利用cgroups来做资源分配

命名空间:

|类型|描述|
|--|--|
|pid命名空间|不同用户的进程就是通过pid命名空间隔离开的|
|net命名空间|网络隔离是通过net命名空间是实现的|
|ipc命名空间|容器中进程交互采用了IPC(interprocess communication)|
|mnt命名空间|类似chroot,将一个进程放到一个特定的目录执行,mnt命名空间允许不同命名空间的进程看到的文件结构不同|
|uts命名空间|UTS(UNIX Time-sharing System)允许每个容器拥有独立的hostname和domain name,使其在网络上可以被视为一个独立的节点而非主机上的一个进程|
|user命名空间|每个容器可以有不同的用户和组id,也就是说可以在容器内用容器内部的用户执行程序而非主机上的用户|

控制组可以提供对容器的内存,CPU,磁盘IO等资源的限制和审计管理

### 资源限制

默认情况下,容器没有资源限制,它会尽可能地使用宿主机能够分配给它的资源

#### 限制内存

在运行容器时可以强制限制容器地资源使用地限制,即只允许容器使用不超过给定数量地系统内存

|选项|描述|
|--|--|
|-m 或 -memory|容器可以使用的最大内存量,最小值为4MB|
|--memory-swap|内存加交换分区的容量|
|--kernel-memory|容器可以使用的最大内核内存量,最小4MB|

#### 限制docker使用CPU

|选项|描述|
|--|--|
|--cpus|指定容器可以使用的可用CPU资源|
|--cpuset-cpu|限制容器可以使用的特定CPU或核心|
