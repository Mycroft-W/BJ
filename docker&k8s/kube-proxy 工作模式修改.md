# Kube-proxy 修改工作模式
kube-proxy工作模式为两种，iptables 和 ipvs 
(1.29版本后新增了 nftables 模式）

使用容器化部署的kube-proxy 配置文件是以configMap形式挂载在容器中的，通过 `kubectl -n kube-system get configmap kube-proxy -oyaml |grep mode`可以查看当前配置，`mode: "" `空为默认iptables，可选为 'iptables'（默认）和 'ipvs'
### 前置步骤
#### 查看内核参数
```shell
sysctl -a |grep -E "net.ipv4.ip_forward = 1|net.bridge.bridge-nf-call-iptables = 1|net.bridge.bridge-nf-call-ip6tables = 1"
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/46412420/1721879937837-1b58525e-8486-4897-b917-e12806546d64.png#averageHue=%232a2625&clientId=u5ae04a79-f3d9-4&from=paste&height=73&id=uec706bf5&originHeight=109&originWidth=1624&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=22624&status=done&style=none&taskId=uda4345a2-3696-4130-bd32-69897b61e02&title=&width=1082.6666666666667)
如果没有通过以下命令添加
```shell
cat >> /etc/sysctl.conf << EOF
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sysctl -p
```
#### 检查主机是否加载了ip_vs mod
```shell
lsmod |grep ip_vs
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/46412420/1721879254721-662bfdeb-2c3b-4635-88d3-6dfca681d7d8.png#averageHue=%23292625&clientId=u5ae04a79-f3d9-4&from=paste&height=96&id=uccefb718&originHeight=144&originWidth=678&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=14863&status=done&style=none&taskId=u8a2859a1-6e0e-4004-b269-521b89e70f9&title=&width=452)
如果没有，通过以下命令加载
```shell
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
```
#### 安装 ipvsadm
```shell
yum install -y ipvsadm
```
### 修改kube-proxy参数
```shell
kubectl -n kube-system edit configmap kube-proxy
# 修改一下两处
mode: "ipvs"
iptables.masqueradeAll: true
```
#### 删除原有pod，重新进行调度
```shell
kubectl get pod -A
kubectl delete pod -all -n kube-system
```
#### 查看kube-proxy 启动日志，查看模式
```shell
kubectl logs kube-proxy-xxx -n kube-system
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/46412420/1721886312887-4c44f1d3-9ceb-4200-9b98-3edff83e910c.png#averageHue=%232d2b2a&clientId=u25f8d29b-c979-4&from=paste&height=413&id=u695098e7&originHeight=620&originWidth=1805&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=199984&status=done&style=none&taskId=u7a9e7ced-0bef-47f6-b201-e370d53017f&title=&width=1203.3333333333333)
#### 查看ipvs维护的ip列表
查看对应service 和endpoints
```shell
ipvsadm -ln
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/46412420/1721885978118-aa026785-8db0-4468-9b0f-f4d9fe5440b1.png#averageHue=%232b2928&clientId=u5ae04a79-f3d9-4&from=paste&height=255&id=u8473f56e&originHeight=383&originWidth=1058&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=70132&status=done&style=none&taskId=u0e8a1e36-c086-4e21-bd9d-1cc7cec4235&title=&width=705.3333333333334)
