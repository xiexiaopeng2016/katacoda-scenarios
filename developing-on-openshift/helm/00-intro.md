## 目标

学习如何使用[Helm](https://helm.sh/) ，这是一个包管理器，可以帮助您管理和部署OpenShift上的应用程序。

![Logo](../../assets/developing-on-openshift/helm/logo.png)

[Helm](https:/helm.sh/) 是Kubernetes的包管理器，它帮助用户创建名为Helm Charts的模板包，以包含部署特定应用程序所需的所有Kubernetes资源。然后Helm协助在Kubernetes上安装Helm Chart，然后当有新版本可用时，它可以升级或回滚所安装的包。

Helm 3是GA版本，在OpenShift 4.4上可用，消除了像Helm 2那样的主要安全隐患。

## 概念

* Helm核心概念
* 探索``helm``命令行工具
* 部署和管理``Helm Charts``
* 创建您自己的``Chart``
* 使用Helm ``Upgrade``和``Rollback``版本管理应用生命周期。
* Helm集成OpenShift用户界面

## 用例

能够为开发人员和系统管理员提供在OpenShift之上使用Helm Charts管理和部署应用程序的良好体验。

Helm图表对于无状态应用程序的安装和升级特别有用，因为Kubernetes资源和应用程序镜像可以简单地更新到较新的版本。第一天的后续体验是，将Helm Charts转换为Operator，使用[Operator Framework](https://github.com/operator-framework) 为你的应用程序提供完整的第二天体验。

OpenShift集群将在一小时内自毁。

让我们开始吧!