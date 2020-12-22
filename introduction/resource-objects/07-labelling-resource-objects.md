当您使用 ``oc new-app`` 部署应用程序时，一个标签将自动应用到所创建的资源对象。标签的名称是 ``app`` ，它将被设置为应用程序的名称。此标签可用于在运行查询时选择资源对象的一个子集。

当您部署了多个应用程序时，您可以使用命令 ``oc get all`` 列出与特定应用程序相关的所有资源对象，并向该命令传递描述要匹配的标签的选择器。

要查询部署的应用程序的资源，请运行:

 ``oc get all -o name --selector app=parksmap``{{execute}}

这应该收益率:

```
pod/parksmap-1-dvsqf
replicationcontroller/parksmap-1
service/parksmap
deploymentconfig.apps.openshift.io/parksmap
imagestream.image.openshift.io/parksmap
route.route.openshift.io/parksmap
route.route.openshift.io/parksmap-fqdn
```

如果需要对资源对象应用附加标签，可以使用 ``oc label`` 命令。

要将标签 ``web`` 添加到应用程序的服务对象，并给它赋值 ``true`` ，运行:

 ``oc label service/parksmap web=true``{{execute}}

然后仅使用该标签查询所有资源对象。

 ``oc get all -o name --selector web=true``{{execute}}

输出中应该只返回服务对象。

要从资源对象中删除标签，你可以使用:

 ``oc label service/parksmap web-``{{execute}}

这个命令中的标签声明是 ``name-`` 格式的。后面的 ``-`` 而不是 ``=value`` 表示应该删除标签。