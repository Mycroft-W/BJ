# kubernetes 安装

本次 kubernetes 部署使用三台机器,一台作为 master 两台作为 node;kubernetes 版本为1.15.1,docker 版本为20.10.5

使用 kubernetes 官方支持的 kubeadm 作为集群部署工具

在 CentOS 7 上安装 kubernetes 之前需要安装一些依赖和对系统进行优化

## 修改主机名,并添加 hosts 信息

|主机名|ip|
|--|--|
|k8s-master01|192.168.10.11|
|k8s-master02|192.168.10.12|
|k8s-master03|192.168.10.13|

修改主机名可以使用:

```shell
hostnamectl set-hostname k8s-master01
```

## 安装依赖

```shell
yum -y install conntrack ntpdate ntp ipvsadm ipset iptalbes curl sysstat libseccomp wget vim net-tools git
```

### 关闭 SELINUX, 禁止使用 swap 分区

```shell
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
setenforce 0
sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
```

## 调整内核参数

```shell
cat > kubernetes.conf <<EOF
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1
net.ipv4.tcp_tw_recycle=0
vm.swappiness=0 # 禁止使用 swap 空间，只有当系统 OOM 时才允许使用它
vm.overcommit_memory=1 # 不检查物理内存是否够用
vm.panic_on_oom=0 # 开启 OOM
fs.inotify.max_user_instances=8192
fs.inotify.max_user_watches=1048576
fs.file-max=52706963
fs.nr_open=52706963
net.ipv6.conf.all.disable_ipv6=1
net.netfilter.nf_conntrack_max=2310720
EOF
cp kubernetes.conf  /etc/sysctl.d/kubernetes.conf
sysctl -p /etc/sysctl.d/kubernetes.conf
```

## 调整系统时区,并同步时间

```shell
# 设置时区为 亚洲/上海
timedatectl set-timezone Asia/Shanghai
# 同步时间
ntpdate ntp1.aliyun.com
# 将当前时间写入 bios
timedatectl set-local-rtc 0
# 重启依赖于时间的服务
systemctl restart rsyslog
systemctl restart crond
```

## 关闭不需要的服务

```shell
systemctl stop postfix
systemctl disable postfix
```

## 设置 rsyslogd 和 systemd journald

```shell
mkdir /var/log/jorunal
mkdir /etc/systemd/journald.conf.d
cat > /etc/systemd/journald.conf.d/99-prophet.conf <<EOF
[Journal]
# 持久化保存到磁盘
Storage=persistent

# 压缩历史日志
Compress=yes

SyncIntervalSec=5m
RateLimitInterval=30s
RateLimitBurst=1000

# 最大占用空间 10G
SystemMaxUse=10G

# 单日志文件最大 200M
SystemMaxFileSize=200M

# 日志保存时间 2 周
MaxRetentionSec=2week

# 不将日志转发到 syslog
ForwardToSyslog=no
EOF
systemctl restart systemd-journald
```

## 升级系统内核

CentOS 7 原先的内核是3.10版本,在运行 Docker 和 Kubernetes 时不是很稳定

```shell
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
# 安装完成后检查 /boot/grub2/grub.cfg 中对应内核 menuentry 中是否包含 initrd16 配置，如果没有，再安装一次！
yum --enablerepo=elrepo-kernel install -y kernel-lt
# 设置开机从新内核启动
grub2-set-default 'CentOS Linux (4.4.189-1.el7.elrepo.x86_64) 7 (Core)'
```

## 启用ip_vs

```shell
modprobe br_netfilter
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4

lsmod |grep -e ip_vs -e nf_conntrack_ipv4
```

## 安装 Docker 软件

```shell
yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager \
  --add-repo \
  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y docker-ce

## 创建 /etc/docker 目录
mkdir /etc/docker

# 配置 daemon.json
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "insecure-registries": ["harbor.hongfu.com"]
}
EOF
mkdir -p /etc/systemd/system/docker.service.d

# 重启docker服务
systemctl daemon-reload
systemctl restart docker
systemctl enable docker
```

## 安装 kubeadm

```shell
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

yum -y  install  kubeadm-1.15.1 kubectl-1.15.1 kubelet-1.15.1
systemctl enable kubelet.service
```

## 初始化主节点

此步骤之前的所有步骤在三台机器上都要做一遍,而主节点的初始化只要一台机器做完后,其他机器作为从节点加入集群即可

首先生成主节点初始化所需配置文件

```shell
  kubeadm config print init-defaults > kubeadm-config.yaml
```

修改其中相应字段,并添加部分信息

```yaml
localAPIEndpoint:
  advertiseAddress: 192.168.10.11   # 修改为本机IP
kubernetesVersion: v1.15.1  # 修改版本号为安装版本
networking:
  podSubnet: "10.244.0.0/16"    # 添加 Pod 网络
  serviceSubnet: 10.96.0.0/12
# 添加以下信息
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
  SupportIPVSProxyMode: true
mode: ipvs
```

执行初始化并保存提示信息

```shell
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log
```

要启动 k8s 集群,需要创建集群用户

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## 其他主机加入集群作为 node 节点

查看 master 初始化后的提示信息,在 node 主机运行提示的命令即可加入集群

```shell
kubeadm join 192.168.10.11:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:38793b41ebcf7b8cd98ed24adac407548e6f4a8e3986b30216170bd464183b4c
```

## 部署网络

在此步骤之前, node 节点已经加入集群但状态为 notready;需要部署
flannel 后才可正常使用

```shell
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
