目前，我们有两个OpenShift集群，其中一个( ``cluster1`` )运行KubeFed控制面板。现在是使用 ``kubefedctl`` 工具注册每个集群的时候了，为了您的方便，该工具已经安装在环境中。

 ``kubefedctl`` 驻留在 [上游回购](https://github.com/kubernetes-sigs/kubefed/) ，可以从发布部分下载。

在注册两个集群之前，我们要检查是否还没有注册集群。

``oc --context=cluster1 get kubefedclusters -n test-namespace``{{execute HOST1}}

没有找到资源message表示还没有注册集群，因此是时候注册两个集群了。

 _注意:_ 下面命令中的集群名称(cluster1和cluster2)是对在oc客户机中配置的上下文的引用。这已经为您配置好了，否则您将需要确保客户端上下文已经正确地配置了正确的访问级别和上下文名称。有关上下文的更多信息，请参阅这里。

为了注册集群，使用 ``kubefedctl`` 工具如下:

 ``kubefedctl join <CLUSTER_NAME> --host-cluster-context <HOST_CLUSTER_CONTEXT> --v=2`` 

 ``kubefedctl join`` 的——cluster-context选项可用于覆盖对客户端上下文配置的引用。如果不提供该选项(如下面的命令中所示)， ``kubefedctl`` 将使用集群名称来标识客户机上下文。

 ``kubefedctl join`` 的——KubeFed -namespace选项可以用来覆盖对运行KubeFed控制平面的名称空间的引用，它默认为 ``federation-namespace`` 。

``kubefedctl join cluster1 --host-cluster-context cluster1 --v=2 --kubefed-namespace=test-namespace``{{execute HOST1}}

现在该注册 ``cluster2`` 了。

``kubefedctl join cluster2 --host-cluster-context cluster1 --v=2 --kubefed-namespace=test-namespace``{{execute HOST1}}

上面的命令将注册为 ``cluster2`` ，并将被视为 ``Member Cluster`` 。

现在，我们可以验证两个集群都已注册:

``oc --context=cluster1 get kubefedclusters -n test-namespace``{{execute HOST1}}

如果一切正常，您应该看到两个集群都已注册，并通过API报告健康状态(这可能需要一些时间):

```
NAME       READY     AGE
cluster1   True      28s
cluster2   True      21s
```