## 目标

了解如何使用OpenShift上的源代码到镜像构建从源代码部署应用程序。

## 概念

* Linux容器和构建容器镜像
* OpenShift Source-to-Image (S2I)
* OpenShift项目和应用程序
* OpenShift`oc`命令行工具

## 用例

你可以让OpenShift从源代码构建一个应用程序来部署它，这样你就不必在每次更改时手工构造一个容器。然后，OpenShift可以在通知源代码更改时自动构建和部署新版本。

这个OpenShift集群将在一小时内自毁。