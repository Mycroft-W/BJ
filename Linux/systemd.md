# Systemd

systemd 是一个替代 sysv 的守护进程，但是相比 sysv 提供了更多的功能

## 系统管理

### systemctl

systemctl 是 systemd 的主命令，用于管理系统

```shell
# 重启系统
$ systemctl reboot

# 关闭系统，切断电源
$ systemctl poweroff

# CPU停止工作
$ systemctl halt

# 暂停系统
$ systemctl suspend

# 让系统进入冬眠状态
$ systemctl hibernate

# 让系统进入交互式休眠状态
$ systemctl hybrid-sleep

# 启动进入救援状态（单用户状态）
$ systemctl rescue
```
#### 运行等级修改

```shell
# 查看默认运行等级
$ systemctl get-default

# 改变默认运行等级
$ systemctl set-default multi-user.target

# 切换运行等级
$ systemctl isolate multi-user.target

```

### systemd-analyze

systemd-analyze 用于查看启动耗时

```shell
# 查看启动耗时
$ systemd-analyze

# 查看每个服务的启动耗时
$ systemd-analyze blame

# 显示瀑布状的启动过程流
$ systemd-analyze critical-chain

# 显示指定服务的启动流
$ systemd-analyze critical-chain <atd.service>
```

### hostnamectl

用于主机信息设置

```shell
# 显示当前主机的信息
$ hostnamectl

# 设置主机名。
$ hostnamectl set-hostname <hostname>
```

### localectl

用于本地化设置

```shell

# 查看本地化设置
$ localectl

# 设置本地化参数。
$ localectl set-locale LANG=zh_CN.utf8
$ localectl set-keymap en_US
```

### timedatectl

用于时间时区的设置

```shell
# 查看当前时区设置
$ timedatectl

# 显示所有可用的时区
$ timedatectl list-timezones

# 设置当前时区
$ timedatectl set-timezone Asia/Shanghai
$ timedatectl set-time YYYY-MM-DD
$ timedatectl set-time HH:MM:SS
```

### loginctl

```shell
# 列出当前session
$ loginctl list-sessions

# 列出当前登录用户
$ loginctl list-users

# 列出显示指定用户的信息
$ loginctl show-user root
```

## Unit

systemd 中的不同系统资源统称为Unit(单位)，分为了12种

|unit名称|解释|
|--|--|
|Service Unit| 系统服务|
|Target Unit| 多个Unit构成的组|
|Device Unit| 硬件设备|
|Mount Unit| 文件系统挂载点|
|Automount Unit| 自动挂载点|
|Path Unit| 文件或路径|
|Scope Unit| 不是由 Systemd 启动的外部进程|
|Slice Unit| 进程组|
|Snapshot Unit| Systemd快照，可以切回某个快照|
|Socket Unit| 进程间通信的 socket|
|Swap Unit| swap 文件|
|Timer Unit| 定时器|

## 服务Unit文件配置

systemd配置文件内容

```service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755
StandardOutput=file:/var/log/service.log
StandardError=file:/var/log/err_service.log

[Install]
WantedBy=multi-user.target
Alias=sshd.service
```

### Unit 区块配置字段
* Description，服务描述
* Documentation，文档位置
* After，需要哪些服务先启动，network.target
* Before，在那些服务前先启动
* Wants，弱依赖关系
* Requires， 强依赖，启动顺序无关

### Service 区块配置字段

* EnviromentFile，当前服务环境便令参数文件，sshd环境参数文件 /etc/sysconfig/sshd
* ExecStart， 定义启动进程时执行的命令
* ExecReload，重启服务时执行的命令
* ExecStop，停止服务时执行的命令
* ExecStartPre，启动服务之前执行的命令
* ExecStartPost，启动服务之后执行的命令
* ExecStopPost，停止服务之后执行的命令
* Type，定义启动类型；simple主进程；forking以fork()方式启动；oneshot，执行一次；dbus，等待D-Bus信号启动；notify，启动后发出信号，然后systemd再启动其他服务；idle，等其他任务执行完，才会启动该服务
* KillMode，定义Systemd如何停止服务；process，只停主进程，不停子进程；control-group，停止控制组里的所有子进程；mixed，主进程收到SIGTERM信号，子进程收到SIGKILL信号；none，执行服务的stop命令
* Restart，退出后，systemd的重启方式；no，退出不重启；on-success，正常退出，才重启；on-failure，非正常退出时，才重启；on-abnormal，被信号终止和超时，才重启；on-watchdog，超时才重启；always，无论如何重启
* RestartSec，重启前等待时间
* StandardOutput，标准日志输出，null表示不输出日志，路径可以控制输出文件位置(对于systemd 236或更高版本，使用StandardOutput=**file:**/some/path)
* StandardError，错误日志输出，同上


### Install 区块配置字段

* WantedBy，服务所在target；multi-user.target等

## 网络管理

systemd 逐渐的接管了许多的系统配置服务，其中网络配置由以下几个服务管理

### systemd-networkd

管理网卡，包括配置 IP， DNS， DHCP 等等；配置文件放在`/etc/systemd/network/`中，简单的配置方式如下

```wired.network
[Match]
Name=eth0   # 使用设备名匹配设备

[Network]
DHCP=yes    # 使用DHCP
```

### systemd-resolved

配置 DNS 服务器，配置文件是`/etc/systemd/resolved.conf`,简单配置如下

```resolve.conf
[Resolve]
DNS=8.8.8.8
```
