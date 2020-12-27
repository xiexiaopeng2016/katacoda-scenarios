 ``oc create`` 命令允许您从一个文件中包含的JSON或YAML定义创建一个新的资源对象。使用 ``oc edit`` 更改现有资源对象是一个交互过程。要想从包含在文件中的JSON或YAML定义中更改现有资源，可以使用 ``oc replace`` 命令。

为了禁止不安全的路由，你需要创建一个经过修改的路由对象定义:

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
            "insecureEdgeTerminationPolicy": "Redirect"
        }
    }
}
!``{{execute}}

然后运行:

 ``oc replace -f parksmap-fqdn.json``{{execute}}

为了让 ``oc replace`` 瞄准正确的资源对象，JSON或YAML定义的 ``metadata.name`` 值必须与要更改的值相同。

要使用 ``oc replace`` 编写现有资源对象中值更新的脚本，需要使用 ``oc get`` 获取现有资源对象的定义。然后可以编辑定义， ``oc replace`` 用于更新现有资源对象。

要编辑定义，需要动态编辑JSON或YAML定义的方法。这个过程的替代方法是使用 ``oc patch`` 命令，该命令将根据提供的规范为您编辑适当的值。

例如， ``route.spec.tls.insecureEdgeTerminationPolicy`` 值可以切换回允许一个不安全的路由，运行:

 ``oc patch route/parksmap-fqdn --patch '{"spec":{"tls": {"insecureEdgeTerminationPolicy": "Allow"}}}'``{{execute}}

对于这两种情况，要更新的资源对象必须已经存在，否则命令将失败。如果您不知道资源对象是否已经存在，并且希望更新它，如果不更新就创建它，那么您可以使用 ``oc apply`` 代替，而不是 ``oc replace``。