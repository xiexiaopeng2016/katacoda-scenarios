[KubeFed](https://github.com/kubernetes-sigs/kubefed) 是一家Kubernetes运营商，提供通过多个Kubernetes集群管理应用程序和服务的工具。

KubeFed允许用户:

* 跨注册的集群分布工作负载

* 用有关这些工作负载的信息编写DNS程序

* 动态调整部署工作负载的不同集群中的副本

* 为这些工作负载提供灾难恢复

随着KubeFed的成熟，我们希望添加与存储管理、工作负载放置等相关的特性。

KubeFed利用了新的机制来扩展Kubernetes API，并为用户提供一个简单的接口来互连他们的Kubernetes集群，而无需处理网络延迟、etcd需求等。

KubeFed控制面板由运行在联邦集群之一上的操作员组成。这个操作员负责一些 [crd](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/) ，这将在后面的课程中讨论。

| 概念 | 定义 |
| ---- | ---- |
| 主机集群 | 一个集群，用于公开KubeFed API并运行KubeFed控制平面 |
| 集群成员 | 一个在KubeFed API中注册的集群，并且KubeFed控制器具有认证凭据。主机集群也可以是成员集群。 |