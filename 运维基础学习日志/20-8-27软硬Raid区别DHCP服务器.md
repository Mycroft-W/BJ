# DHCP

## 软硬RAID区别

软RAID：通过用操作系统来完成RAID功能的就是软RAID
    1. 插入硬盘,分区格式化
    2. 安装操作系统
    3. 构建RAID

硬RAID：全部通过用硬件来实现RAID功能的就是硬RAID（缺陷：每个品牌的RAID不通用）
    1. 插入硬盘
    2. 通过RAID卡组建RAID
    3. 安装操作系统,分区,格式化

## DHCP服务

DHCP(Dynamic Host Configuration Protocol)动态主机配置协议

使用DHCP的好处

1. 减少管理员的工作量
2. 避免输入错误的可能
3. 避免IP冲突
4. 提高IP地址利用率
5. 方便客户端的配置

### DHCP的租约过程

1. 客户端请求IP（发起DHCPDISCOVER广播包）

    | 局域网内DHCP服务器数量 | 客户端                                                       |
    | ---------------------- | ------------------------------------------------------------ |
    | 0                      | 持续广播（xp以前不停,win7之后无响应DHCP服务器给自己分配一个169开头的假IP |
    | 1                      | 正常完成请求,获取IP                                         |
    | n                      | 先到先得                                                     |

2. 服务器响应（发DHCPOFFER广播包）

    服务器会对IP进行测试,防止占用(使用ICMP协议)

3. 客户端选择IP（发DHCPREQUEST广播包）

    过程中客户端会对IP进行测试,防止占用(使用ARP协议)

4. 服务器确定租约（发DHCPACK/DHCPNAK广播包）*租约为有线8天,无线8小时*

![DHCP租约](./Pics/DHCP租用.png)

### DHCP续租过程

1. 客户端使用租约达到50%；开始向服务器发起单播(REQUEST包),续租

2. 服务器无法连接,继续使用租约,到87.5%发起（REQUEST包）广播,续租

3. 无可用服务器,继续使用租约,到100%；向局域网发起（DISCOVER包）广播,查询新的DHCP服务器,重新租用IP

![DHCP续租](./Pics/DHCP续租.png)

### DHCP实验（Windows）

1. 虚拟机桥接网路

2. 服务器端（虚拟机）需要有固定IP地址

    安装DHCP服务（随向导进行配置,安装成功后即可使用）

### 客户端常用命令

```bash
ipconfig # 查询网络信息
ipconfig /release # 释放获取的IP地址
ipconfig /renew # 重新获取IP地址
```
