现在你已经创建了一个要使用的应用程序，已经在项目中创建的关键资源对象的列表可以使用:

 ``oc get all``{{execute}}

命令。运行此命令后，您将看到类似如下的输出:

```
NAME                    READY   STATUS              RESTARTS   AGE
pod/parksmap-1-deploy   1/1     Running             0          22s
pod/parksmap-1-dvsqf    0/1     ContainerCreating   0          9s

NAME                               DESIRED   CURRENT   READY   AGE
replicationcontroller/parksmap-1   1         1         0       22s

NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/parksmap   ClusterIP   172.30.222.21   <none>        8080/TCP   23s

NAME                                          REVISION   DESIRED   CURRENT   TRIGGERED BY
deploymentconfig.apps.openshift.io/parksmap   1          1         1         config,image(parksmap:1.0.0)

NAME                                      IMAGE REPOSITORY TAGS    UPDATED
imagestream.image.openshift.io/parksmap   default-route-openshift-image-registry.apps-crc.testing/myproject/parksmap 1.0.0   23 seconds ago

NAME                                HOST/PORT                                                            PATH   SERVICES   PORT       TERMINATION   WILDCARD
route.route.openshift.io/parksmap   parksmap-myproject.2886795273-80-frugo03.environments.katacoda.com          parksmap   8080-tcp                 None
```

你可以通过运行以下命令来限制输出，只输出资源的名称:

 ``oc get all -o name``{{execute}}

换句话说，提供 ``-o name`` 选项来更改输出格式。

```
pod/parksmap-1-deploy
pod/parksmap-1-dvsqf
replicationcontroller/parksmap-1
service/parksmap
deploymentconfig.apps.openshift.io/parksmap
imagestream.image.openshift.io/parksmap
route.route.openshift.io/parksmap
```

 ``oc get`` 命令是OpenShift中用于查询资源对象的最基本的命令。您将经常使用它，因此您应该熟悉它，以及如何更新资源对象。

除了能够使用特殊名称 ``all`` 来查询有关关键资源对象类型的信息之外，还可以按名称列出特定的对象类型。例如，你可以通过运行得到应用程序公开时创建的路由列表:

 ``oc get routes``{{execute}}

对于你已经部署的应用程序，你应该看到这样的东西:

```
NAME       HOST/PORT                                                            PATH   SERVICES   PORT       TERMINATION   WILDCARD
parksmap   parksmap-myproject.2886795273-80-frugo03.environments.katacoda.com          parksmap   8080-tcp     None
```

通过运行以下命令，你可以得到所有不同资源对象类型的列表:

 ``oc api-resources``{{execute}}

这将输出一个以如下方式开始的长列表:

```
NAME                                  SHORTNAMES       APIGROUP                              NAMESPACED   KIND
bindings                                                                                     true         Binding
componentstatuses                     cs                                                     false        ComponentStatus
configmaps                            cm                                                     true         ConfigMap
endpoints                             ep                                                     true         Endpoints
events                                ev                                                     true         Event
limitranges                           limits                                                 true         LimitRange
namespaces                            ns                                                     false        Namespace
nodes                                 no                                                     false        Node
...
```

除了能够使用全名查询资源对象类型之外，还可以使用较短的别名查询许多资源对象类型。因此，你可以用 ``cm`` 代替 ``configmaps`` 。

在资源对象的 ``type`` 作为复数列出的所有情况下，您也可以使用 ``type`` 的单数形式。因此你可以用 ``route`` 代替 ``routes`` 。