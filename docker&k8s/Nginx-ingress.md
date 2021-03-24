# Nginx-ingress

Nginx-ingress controller 是 kubernetes 中 ingress controller 的一个基于 nginx 实现,安装后可以在 kubernetes 集群中实现 ingress 对象的创建以及调度

本次文仅演示部分nginx-ingress 功能,ingress 的详细信息可以阅读[kuberntetes](./Kubernetes.md)获取; nginx-ingress 的更详细使用方法请参阅[nginx-ingress官网文档](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/)

## 安装

官方提供了多种的安装方法[nginx-ingress部署](https://kubernetes.github.io/ingress-nginx/deploy/#installation-guide)

本次示例基于 CentOS 7 的 kubernetes 集群,通过以下命令部署:

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/baremetal/deploy.yaml
```

## 代理 HTTP

deployment 提供真实的服务 Pod, Service 对集群内部暴露服务, Ingress 通过代理对外暴露服务

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    name: nginx
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  rules:
    - host: www.test.com
      http:
        paths:
        - path: /
          backend:
            serviceName: nginx-svc
            servicePort: 80
```

## 代理 HTTPS

需要先创建包含证书和私钥的 Secret 对象

```shell
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=nginxsvc/O=nginxsvc"    # 生成伪造的证书和私钥

kubectl create secret tls tls-secret --key tls.key --cert tls.crt   # 用证书和私钥生成 Secret
```

在 Ingress 资源清单中添加 tls 字段

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  tls:
    - hosts:
      - www.test.com
      secretName: tls-secret
  rules:
    - host: www.test.com
      http:
        paths:
        - path: /
          backend:
            serviceName: nginx-svc
            servicePort: 80
```

## BasicAuth

进行基本的认证,与平常 nginx 服务器的验证方法基本一致

首先,生成认证文件;然后创建 Secret 对象

```shell
yum -y install httpd
htpasswd -c auth foo            # 生成认证文件,文件名auth,用户foo
kuberctl create secret generic basic-auth --form-file=auth
```

然后在 Ingress 清单中写入标注(annotations)

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-with-auth
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic            # 认证方式
    nginx.ingress.kubernetes.io/auth-secret: basic-auth     # 认证资源
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - foo' # 认证用户
spec:
  rules:
  - host: foo2.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

## 重写

nginx-ingress 提供了以下接口用于配置重写方法:

|接口|描述|值|
|--|--|--|
|nginx.ingress.kubernetes.io/rewrite-target| 必须重定向流量的目标URI| 字符串 |
|nginx.ingress.kubernetes.io/ssl-redirect|指示位置部分是否仅可访问SSL（当Ingress包含证书时默认为True）| 布尔值 |
|nginx.ingress.kubernetes.io/force-ssl-redirect| 即使Ingress未启用TLS，也强制重定向到HTTPS| 布尔值 |
|nginx.ingress.kubernetes.io/app-root| 定义Controller必须重定向的应用程序根，如果它在'/'上下文中| 字符串   |
|nginx.ingress.kubernetes.io/use-regex| 指示Ingress上定义的路径是否使用正则表达式| 布尔值 |

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: https://foo.bar.com:32127
spec:
  rules:
  - host: www.test.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```
