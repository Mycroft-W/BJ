# Linux 中常用服务软件

## ssh 服务

**名称**: ssh 安全远程连接服务

**软件**: openssh openssh-clients openssh-server

**服务**: sshd

**端口**: TCP 22

**配置文件**:

Server 配置文件: /etc/ssh/sshd_config

Client 配置文件: /etc/ssh/ssh_config

## DHCP 服务

**名称**: DHCP 动态主机配置服务

**软件**: dhcp dhcp-common

**服务**: dhcpd

**端口**:

   UDP 67 (接收端口)

   UDP 68 (发送端口)

**配置文件**:

/etc/dhcp/dhcpd.conf

## DNS 服务

**名称**: DNS 域名解析服务

**软件**: bind

**服务**: named

**端口**:

   UDP 53 (数据通信,域名解析)

   TCP 53 (数据同步,主从同步)

**配置文件**:

主配置文件: /etc/named.conf

区域配置文件: /etc/named.rfc1912.zones

数据配置文件: /var/named/xxxx(与区域配置中相同)

## FTP 服务

**名称**: VSFTP 互联网文件传输

**软件**: vsftpd

**服务**: vsftpd

**端口**: TCP 20 21

**配置文件**:

   主配置文件: /etc/vsftpd/vsftpd.conf

## SAMBA 服务

**名称**: samba 局域网文件传输

**软件**: samba

**服务**: smb

**端口**: TCP 139 445

**配置文件**:

主配置文件: /etc/samba/smb.conf

## TCP Wrappers

**名称**: TCP Wrappers TCP 简单防火墙

**软件**: tcp_wrappers

**配置文件**:

   黑名单: /etc/hosts.deny

   白名单: /etc/hosts.allow
