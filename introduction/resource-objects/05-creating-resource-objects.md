 ``oc edit`` 命令将被用来改变一个现有的资源对象，它不能被用来创建一个新的对象。要创建一个新对象，您需要使用 ``oc create`` 命令。

 ``oc create`` 命令提供了一种从JSON或YAML定义创建任何资源对象的通用方法，以及针对资源对象类型子集的一种更简单的选项驱动方法。

例如，如果你想用你自己的主机名为应用程序创建一个安全路由，你可以创建一个包含路由定义的 ``parksmap-fqdn.json`` 文件:

 ``cat > parksmap-fqdn.json << !
{
    "kind": "Route",
    "apiVersion": "v1",
    "metadata": {
        "name": "parksmap-fqdn",
        "labels": {
            "app": "parksmap"
        }
    },
    "spec": {
        "host": "www.example.com",
        "to": {
            "kind": "Service",
            "name": "parksmap",
            "weight": 100
        },
        "port": {
            "targetPort": "8080-tcp"
        },
        "tls": {
            "termination": "edge",
            "insecureEdgeTerminationPolicy": "Allow"
        }
    }
}
!``{{execute}}

要从 ``parksmap-fqdn.json`` 文件创建路由，你可以运行以下命令:

 ``oc create -f parksmap-fqdn.json``{{execute}}。

这个路由的定义对 ``route.metadata.name`` 有一个唯一的值，它以前没有使用过。如果你现在运行:

 ``oc get routes``{{execute}}

您应该会看到列出了两条路由。

```
NAME            HOST/PORT                                                            PATH   SERVICES   PORT       TERMINATION   WILDCARD
parksmap        parksmap-myproject.2886795273-80-frugo03.environments.katacoda.com          parksmap   8080-tcp          None
parksmap-fqdn   www.example.com                                                             parksmap   8080-tcp   edge/Allow    None
```

在路由的情况下， ``oc create`` 提供了一个子命令，专门用于创建路由。因此，你也可以运行 ``oc create route`` 使用命令:

 ``oc create route edge parksmap-fqdn --service parksmap --insecure-policy Allow --hostname www.example.com`` 

要查看 ``oc create`` 具有更具体支持的资源对象类型列表，请运行:

 ``oc create --help``{{execute}}