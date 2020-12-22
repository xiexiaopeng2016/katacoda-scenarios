## 目标

了解如何在OpenShift上使用持久存储运行数据库。使用命令行shell访问集群中的数据库服务器，然后使用端口转发临时公开OpenShift外部的数据库服务，这样您就可以使用任何数据库API工具(比如图形化数据库管理器)访问它。

## 概念

* OpenShift集群上的持久卷存储
* 临时路由外部流量到群集服务
* OpenShift项目和应用程序
* OpenShift `oc` 命令行部署工具

## 用例

您可以在OpenShift集群上部署应用程序的底层数据库服务器，通过开发逐步发展到一个自动化 [操作](https://www.openshift.com/learn/topics/operators) 封装的生产数据库。

这个OpenShift集群将在一小时内自毁。