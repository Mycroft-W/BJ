# Cobbler

Cobbler 是 Red Hat 公司推出的网络安装服务器套件,简化了网络装机的配置,并且可以安装不同的操作系统

## Cobbler 部署

本次使用 Centos7 作为服务器提供网络装机;配置过程大同小异,使用其它系统可以作为参照

首先安装 cobbler 和依赖

```shell
yum install -y epel-release
yum install -y cobbler cobbler-web pykickstart debmirror xinetd
systemctl restart httpd
systemctl restart cobblerd
```

然后修改 cobbler 的配置文件`/etc/cobbler/settings`中的,以下两个字段

```conf
server
next_server
```

修改 `/etc/debmirror.conf`

```conf
    # @dists="sid";
    # @arches="i386";
```

生成 root 密码

```shell
openssl passwd -1 -salt $(openssl rand -hex 4)
```

修改`/etc/cobbler/settings`

```conf
    default_password_crypted
```

安装 cman, fence-agents

```shell
yum install cman fence-agents
```

修改 xinetd 配置`/etc/xinetd.d/tftp`,开启 tftp 服务

```shell
    disabled=no
```

重启,并同步 cobbler 设置,然后检查是否正确

```shell
systemctl restart cobblerd
cobbler sync
cobbler check
```

安装 dhcp 服务

```shell
yum install -y dhcp
```

修改 dhcp 配置文件`/etc/dhcp/dhcpd.conf`

```conf
option domain-name "chinasoft.com";
option domain-name-servers 114.114.114.114,8.8.8.8;
default-lease-time 43200;
max-lease-time 86400;
log-facility local7;
subnet 20.0.0.0 netmask 255.0.0.0 {
    range 20.20.10.10 20.20.10.240;
    option routers 20.20.20.20;
}
next-server 20.20.20.20;
filename="pxelinux.0";
```

重启一系列服务

```shell
systemctl restart dhcpd
systemctl enable tftp
systemctl enable dhcpd
systemctl start tftp
systemctl restart cobblerd
cobbler distro list             # 查看镜像
cobbler profile list            # 查看配置文件
```

## Cobbler 部署 Centos7

挂载 Centos7 的安装镜像,修改 cobbler 的配置文件

```shell
mount -r /dev/cdrom /media                                  # 挂载安装镜像
cobbler import --name="centos7.1810" --path=/media          # 导入镜像文件
cobbler profile remove --name=centos7.1810                  # 删除原本配置文件
cp anaconda-ks.cfg /var/lib/cobbler/kickstarts/centos1.1810.cfg # 复制 kickstart 脚本
cobbler profile add --name=centos7.1810 --distro=centos7.1810 --kickstart=/var/lib/cobbler/kickstarts/centos7.1810.cfg    # 添加配置并指定镜像和安装脚本
cobbler sync                                                # 同步配置
```

修改 kickstart 脚本如下

```conf
#Kickstart Configurator
#platform=x86, AMD64, or Intel EM64T
#System  language
lang en_US
#System keyboard
keyboard us
#Sytem timezone
timezone Asia/Shanghai
#Root password
rootpw --iscrypted $default_password_crypted
#rootpw --iscrypted $1$ops-node$7hqdpgEmIE7Z0RbtQkxW20
#Use text mode install
text
#Install OS instead of upgrade
install
#Use NFS installation Media
url --url="http://192.168.66.14/cobbler/ks_mirror/centos7"          # 修改为自己服务器的地址目录
#System bootloader configuration
bootloader --location=mbr
#Clear the Master Boot Record
zerombr
#Partition clearing information
clearpart --all --initlabel 
#Disk partitioning information
part /boot --fstype xfs --size 1024 --ondisk sda
part swap --size 4000 --ondisk sda
part / --fstype xfs --size 1 --grow --ondisk sda
#System authorization infomation
auth  --useshadow  --enablemd5 
#Network information
$SNIPPET('network_config')
#network --bootproto=dhcp --device=eth0 --onboot=on
# Reboot after installation
reboot
#Firewall configuration
firewall --disabled 
#SELinux configuration
selinux --disabled
#Do not configure XWindows
skipx
%pre
$SNIPPET('log_ks_pre')
$SNIPPET('kickstart_start')
$SNIPPET('pre_install_network_config')
# Enable installation monitoring
$SNIPPET('pre_anamon')
%end
#Package install information
%packages
@^minimal
@core
chrony
kexec-tools
%end
```

## Cobbler 部署 Centos6

Cobbler 部署 Centos6 的配置流程与部署 Centos7 的流程基本一致,但 kickstart 脚本需要修改

```conf
#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth  --useshadow  --enablemd5
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
#Partition information
part /boot --fstype ext4 --size 1024 --ondisk sda
part swap --size=1500
part / --fstype ext4 --size 1 --grow --ondisk sda

# Use text mode install
text
# Firewall configuration
firewall --disable
# Run the Setup Agent on first boot
firstboot --disable
# System keyboard
keyboard us
# System language
lang en_US
# Use network installation
url --url=$tree
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.
$yum_repo_stanza
# Network information
$SNIPPET('network_config')
#network --bootproto=dhcp   --device=em1
# Reboot after installation
reboot

#Root password
rootpw --iscrypted $default_password_crypted
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# System timezone
timezone   Asia/Shanghai
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr

%packages
@base
@compat-libraries
@debugging
@development
tree
nmap
sysstat
lrzsz
dos2unix
telnet

%pre
$SNIPPET('log_ks_pre')
$SNIPPET('kickstart_start')
$SNIPPET('pre_install_network_config')
# Enable installation monitoring
$SNIPPET('pre_anamon')

%post

%end
```
