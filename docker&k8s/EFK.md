# EFK

EFK 不是一个软件,而是一套日志收起分析的解决方案;是在原有的 ELK 的方案基础上使用 Fluentd 或 Filebeat 替换掉 Logstash;相比 Logstash, fluentd 的资源损耗较小

ELK(Elasticsearch, Logstash, Kibana)是曾经业界中最常使用的日志收集分析展示方案

* Elasticsearch 是实时全文搜索和分析引擎,提供搜集,分析,存储数据三大功能
* Logstash 是一个搜索,分析,过滤日志的工具
* Kibana 是一个基于 Web 的图形界面,用于搜索,分析和可视化存储在 Elasticsearch 指标中的日志数据

在 k8s 集群中使用 Helm 部署 EFK 还是比较简单的

## 添加 Google incubator 仓库

```shell
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
```

## 部署 Elasticsearch

```shell
kubectl create namespace efk                # 创建 EFK namespace
helm fetch incubator/elasticsearch          # helm 下载镜像
helm  install --name els1 --namespace=efk -f values.yaml incubator/elasticsearch    # 部署
kubectl  run cirror-$RANDOM --rm -it --image=cirros -- /bin/sh  # 运行 cirror 镜像

> curl Elasticsearch:Port/_cat/nodes    # 查看资源
```

## 部署 Fluentd

```shell
helm fetch stable/fluentd-elasticsearch
vim  values.yaml                    # 更改其中 Elasticsearch 访问地址
helm install --name flu1 --namespace=efk -f values.yaml stable/fluentd-elasticsearch
```

## 部署 Kibana

```shell
helm fetch stable/kibana --version 0.14.8
helm install --name kib1 --namespace=efk -f values.yaml stable/kibana --version 0.14.8
```
