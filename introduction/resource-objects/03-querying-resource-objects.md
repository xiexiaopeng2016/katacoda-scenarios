要获得特定资源对象的更详细描述，可以使用 ``oc describe`` 命令。

运行:

 ``oc describe route/parksmap``{{execute}}

它应该产生类似的结果:

```
Name:                   parksmap
Namespace:              myproject
Created:                5 minutes ago
Labels:                 app=parksmap
Annotations:            openshift.io/host.generated=true
Requested Host:         parksmap-myproject.2886795273-80-frugo03.environments.katacoda.com
                          exposed on router default (host apps-crc.testing) 5 minutes ago
Path:                   <none>
TLS Termination:        <none>
Insecure Policy:        <none>
Endpoint Port:          8080-tcp

Service:        parksmap
Weight:         100 (100%)
Endpoints:      10.128.0.220:8080
```

当将特定的资源对象作为参数传递给 ``oc`` 命令时，可以使用两种约定。第一种方法是使用 ``type/name`` 形式的单个字符串。第二种方法是将 ``type`` 和 ``name`` 作为独立的连续参数传递。命令:

 ``oc describe route parksmap``{{execute}}

是等价的。

 ``oc describe`` 产生的输出是一种人类可读的格式。要以JSON或YAML的形式获取原始对象的详细信息，可以使用 ``oc get`` 命令，列出资源的名称和输出格式。

对于JSON输出，你可以使用:

 ``oc get route/parksmap -o json``{{execute}}。

对于YAML输出，您可以使用:

 ``oc get route/parksmap -o yaml``{{execute}}。

要查看原始对象中特定字段用途的描述，可以使用 ``oc explain`` 命令，为字段提供路径选择器。

要查看 ``spec`` 对象的 ``host`` 字段的描述，你可以运行:

 ``oc explain route.spec.host``{{execute}}

这将输出:

```
KIND:     Route
VERSION:  route.openshift.io/v1

FIELD:    host <string>

DESCRIPTION:
     host is an alias/DNS that points to the service. Optional. If not specified
     a route name will typically be automatically chosen. Must follow DNS952
     subdomain conventions.
```