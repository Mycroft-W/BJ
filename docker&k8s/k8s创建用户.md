# k8s 创建用户并授权

在 k8s 中由于不能直接创建用户，所以需要借助证书申请来产生用户

可以使用 CFSSL 工具来批量申请证书，而 k8s 集群中证书又分为以下几种：

* client certificate： 用于服务端认证客户端
* server certificate： 用户客户端认证服务端
* peer certificate： 双向证书

CFSSL 下载

```shell
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
mv cfssl_linux-amd64 /usr/local/bin/cfssl

wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
mv cfssljson_linux-amd64 /usr/local/bin/cfssljson

wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
mv cfssl-certinfo_linux-amd64 /usr/local/bin/cfssl-certinfo
```

编写用来生成申请文件的 json 文件

```json
{
  "CN": "devuser",                      // common name, 作为集群用户名
  "hosts": [],
  "key": {
    "algo": "rsa",                      // 加密方式
    "size": 2048                        // 加密长度
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",                      // 作为组
      "OU": "System"
    }
  ]
}
```

使用工具生成证书,私钥

```shell
cfssl gencert -ca=ca.crt -ca-key=ca.key -profile=kubernetes /root/devuser-csr.json | cfssljson -bare devuser

# -ca 签名用的根证书
# -ca-key 根证书私钥
# -profile 生成证书的配置
```

在有了证书后,来生成 k8s 用户的配置文件

```shell
# 设置集群参数,apiserver 地址
export KUBE_APISERVER="https://172.20.0.113:6443"

# 将集群的证书写入配置文件
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${KUBE_APISERVER} \
--kubeconfig=devuser.kubeconfig

# 设置客户端认证参数,将用户的证书私钥写入配置文件
kubectl config set-credentials devuser \
--client-certificate=/etc/kubernetes/ssl/devuser.pem \
--client-key=/etc/kubernetes/ssl/devuser-key.pem \
--embed-certs=true \
--kubeconfig=devuser.kubeconfig

# 设置上下文参数,互相认证的双方
kubectl config set-context kubernetes \
--cluster=kubernetes \
--user=devuser \
--namespace=dev \
--kubeconfig=devuser.kubeconfig

# 设置默认上下文
kubectl config use-context kubernetes --kubeconfig=devuser.kubeconfig
# 将用户配置文件放入用户家目录
cp -f ./devuser.kubeconfig /root/.kube/config
# 创建角色绑定,并将集群角色admin绑定至用户,并指定 namespace
kubectl create rolebinding devuser-admin-binding --clusterrole=admin --user=devuser --namespace=dev
```

这样就完成了 k8s 集群用户的创建以及角色绑定

使用 dev 用户登录linux 后,管理 k8s 时就只能管理 namespace=dev 的资源了
