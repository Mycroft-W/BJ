# Docker-cheatsheet

## 容器

### 生命周期

```shell
docker create                   # 创建容器

docker rename                   # 容器重命名

docker run                      # 启动容器

docker rm                       # 容器删除

docker update                   # 更新容器资源限制
```

### 启动,停止

```shell
docker start                    # 启动

docker stop                     # 停止

docker restart                  # 重启

docker pause                    # 暂停

docker unpause                  # 恢复

docker wait                     # 阻塞

docker kill                     # 发送 SIGKILL 到容器

docker attach                   # 连接到正在运行的容器
```

### 约束

```shell
docker run --cpuset-cpus=0,2    # 指定 CPU

docker run --cpu-shares=512     # 使用 CPU 量

docker run -m 300M              # 设置内存
```

### 信息

```shell
docker ps                       # 显示在运行的容器

docker logs                     # 容器日志

docker inspect                  # 查看所有信息

docker events                   # 获取容器事件

docker port                     # 显示端口

dcoker top                      # 显示容器中的进程

docker stats                    # 容器资源使用统计

docker diff                     # 容器更改的文件
```

### 导入,导出

```shell
docker cp                       # 在容器和本地复制文件

docker export                   # 将容器导出为 tarball
```

### 执行命令

```shell
docker exec                     # 在容器中执行命令
```

## 镜像

### 镜像生命周期

```shell
docker images                   # 显示镜像

docker import                   # 从 tarball 导入镜像

docker build                    # 从 Dockerfile 构建

docker commit                   # 从容器创建镜像

docker rmi                      # 删除镜像

docker load                     # 从 tar 加载镜像

docker save                     # 保存容器到 tar
```

### 镜像信息

```shell
docker history                  # 镜像历史

docker tag                      # 标记镜像
```

## docker 信息

```shell
docker version                  # docker 版本

docker info                     # docker 配置信息
```

## image

```shell
docker image ls                 # 显示

docker image build              # 构建

docker image history            # 历史

docker image import             # 导入

docker image tag                # 标记

docker image load               # 载入

docker image prune              # 清理

docker image pull               # 拉取

docker image push               # 推送

dcoker image save               # 保存
```

## container

```shell
docker container attach         # 连接到容器内部

docker container commit         # 提交容器成为镜像

docker container cp             # 复制文件

docker container create         # 创建容器

docker container diff           # 显示容器变化

docker container exec           # 在容器中执行命令

docker container export         # 将容器保存为 tar存档

docker container inspect        # 查看容器详情

docker container kill           # 发送信号

docker container logs           # 查看容器日志

docker container ls             # 查看容器

docker container start          # 容器开始

docker container stop           # 容器停止

docker container restat         # 重启容器

docker container rename         # 重命名容器

docker container top            # 查看容器资源
```

## Networks

```shell
docker network create               # 创建网络

docker network rm                   # 删除网络

docker network ls                   # 显示以创建的网络

docker network inspect              # 查看网络详情

docker network connect              # 将容器连接到网络

docker network disconnect           # 将容器断开网络
```

## 仓库

```shell
docker login                    # 登录仓库

docker logout                   # 登出仓库

docker search                   # 在仓库中搜索镜像

docker pull                     # 拉取

docker push                     # 推送
```

## 卷

```shell
docker volume create            # 创建卷

docker volume rm                # 删除卷

docker volume ls                # 显示卷

docker volume inspect           # 查看卷的详细信息

docker volume prune             # 清理卷
```
