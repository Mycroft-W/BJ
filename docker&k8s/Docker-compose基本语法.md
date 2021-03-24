# Docker-compose 基本语法

```yaml
version: '2'
services:
  web:
    image: dockercloud/hello-world
    ports:
      - 8080
    networks:
      - front-tier
      - back-tier
 
  redis:
    image: redis
    links:
      - web
    networks:
      - back-tier
 
  lb:
    image: dockercloud/haproxy
    ports:
      - 80:80
    links:
      - web
    networks:
      - front-tier
      - back-tier
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock 
 
networks:
  front-tier:
    driver: bridge
  back-tier:
driver: bridge
```

## 1、image

```yaml
services:
  web:
    image: hello-world
```

```yaml
# 镜像可用格式
image: redis
image: ubuntu:14.04
image: tutum/influxdb
image: example-registry.com:4000/postgresql
image: a4bc65fd
```

## 2、build

服务除了可以基于指定的镜像，还可以基于一份 Dockerfile，在使用 up 启动之时执行构建任务，这个构建标签就是 build，它可以指定 Dockerfile 所在文件夹的路径。Compose 将会利用它自动构建这个镜像，然后使用这个镜像启动服务容器

```yaml
build: /path/to/build/dir
```

也可以是相对路径，只要上下文确定就可以读取到 Dockerfile

```yaml
build: ./dir
```

```yaml
build:
  context: ../
  dockerfile: path/of/Dockerfile
   args:
    buildno: 1
    password: secret
image: webapp:tag
```

## 3、command

```yaml
command: bundle exec thin -p 3000
# == 
command: [bundle, exec, thin, -p, 3000]
```

## 4、container_name：<项目名称><服务名称><序号>

```yaml
container_name: app
```

## 5、depends_on

```yaml
version: '2'
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres
```

## 6、dns

```yaml
dns: 8.8.8.8

dns:
  - 8.8.8.8
  - 9.9.9.9
```

## 7、tmpfs

```yaml
tmpfs: /run
tmpfs:
  - /run
  - /tmp
```

## 8、 entrypoint

```yaml
entrypoint: /code/entrypoint.sh
```

## 9、env_file

```yaml
env_file: .env


env_file:
  - ./common.env
  - ./apps/web.env
  - /opt/secrets.env
```

## 10、environment：镜像变量

```yaml
environment:
  RACK_ENV: development
  SHOW: 'true'
  SESSION_SECRET:
 
environment:
  - RACK_ENV=development
  - SHOW=true
  - SESSION_SECRET
```

## 11、expose

```yaml
expose:
 - "3000"
 - "8000"
```

## 12、 external_links：链接外部容器

```yaml
external_links:
 - redis_1
 - project_db_1:mysql
 - project_db_1:postgresql
```

## 13、extra_hosts

```yaml
extra_hosts:
 - "somehost:162.242.195.82"
 - "otherhost:50.31.209.229"
```

## 14、labels

```yaml
labels:
  com.example.description: "Accounting webapp"
  com.example.department: "Finance"
  com.example.label-with-empty-value: ""
labels:
  - "com.example.description=Accounting webapp"
  - "com.example.department=Finance"
  - "com.example.label-with-empty-value"
```

## 15、links：与 Docker client 的 --link 一样效果，会连接到其它服务中的容器

```yaml
links:
 - db
 - db:database
 - redis
```

## 16、 logging

```yaml
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

## 17、pid

```yaml
pid: "host"
```

## 18、port

```yaml
ports:
 - "3000"
 - "8000:8000"
 - "49100:22"
 - "127.0.0.1:8001:8001"
```

## 19、security_opt

```yaml
# 为每个容器覆盖默认的标签。简单说来就是管理全部服务的标签。比如设置全部服务的user标签值为USER。
security_opt:
  - label:user:USER
  - label:role:ROLE
```

## 20、 stop_signal

```yaml
stop_signal: SIGUSR1
```

## 21、volumes

```yaml
volumes:
  // 只是指定一个路径，Docker 会自动在创建一个数据卷（这个路径是容器内部的）。
  - /var/lib/mysql
 
  // 使用绝对路径挂载数据卷
  - /opt/data:/var/lib/mysql
 
  // 以 Compose 配置文件为中心的相对路径作为数据卷挂载到容器。
  - ./cache:/tmp/cache
 
  // 使用用户的相对路径（~/ 表示的目录是 /home/<用户目录>/ 或者 /root/）。
  - ~/configs:/etc/configs/:ro
 
  // 已经存在的命名的数据卷。
  - datavolume:/var/lib/mysql
```

## 22、volumes_from：从其它容器或者服务挂载数据卷，可选的参数是 :ro或者 :rw，前者表示容器只读，后者表示容器对数据卷是可读可写的。默认情况下是可读可写的

```yaml
volumes_from:
  - service_name
  - service_name:ro
  - container:container_name
  - container:container_name:rw
```

## 23、cap_add, cap_drop

```yaml
cap_add:
  - ALL
 
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

## 24、extends

```yaml
extends:
  file: common.yml
  service: webapp
```

## 25、network_mode

```yaml
network_mode: "bridge"
network_mode: "host"
network_mode: "none"
network_mode: "service:[service name]"
network_mode: "container:[container name/id]"
```

## 26、 networks

```yaml
services:
  some-service:
    networks:
     - some-network
     - other-network
```

## Example

```yaml
version: '2'

services:
   db:
     image: mysql:5.7
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: somewordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     restart: always
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
```
