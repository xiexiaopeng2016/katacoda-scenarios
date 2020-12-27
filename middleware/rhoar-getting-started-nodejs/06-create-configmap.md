可以通过几种不同的方式创建configmap。对于本例，我们将使用 **oc** 命令创建一个基于示例应用程序中包含的 ``app-config.yml`` 文件内容的ConfigMap。

 **1. 分配权限**

要访问configmap的应用程序需要这样做的权限。单击下面的命令授予访问应用程序:

``oc policy add-role-to-user view -n $(oc project -q) -z default``{{execute}}

 **2. 使用 `oc` 创建ConfigMap**

单击下面的命令创建ConfigMap对象。因为你已经登录OpenShift，并且目前在 ``example`` 项目中，ConfigMap将在那里创建，并可从运行在该项目中的应用程序访问。

``oc create configmap app-config --from-file=app-config.yml``{{execute}}

名称 ``app-config`` 与在运行时访问ConfigMap的代码 ``app.js`` 中使用的名称相同。

 **3. 验证您的ConfigMap配置已经部署**

``oc describe cm app-config``{{execute}}

> 注意: ``cm`` 是 ``configmap`` 的简写

你应该可以在终端窗口中看到ConfigMap的内容:

```console
Name:           app-config
Namespace:      example
Labels:         <none>
Annotations:    <none>

Data
====
app-config.yml:
----
message : "Hello, %s from a ConfigMap !"

Events: <none>
```

ConfigMap的 ``Data`` 值包含键/值对，在本例中是 ``app-config.yml`` 的键(从初始化ConfigMap的文件的名称)其中包含配置值。在运行时，您在最后一步中编写的代码使用这些名称访问ConfigMap读取内容(在本例中，我们在应用程序中使用 ``message`` 值来定制返回的消息运行时)。

现在您已经编写了用于读取ConfigMap的应用程序代码，并创建了ConfigMap，是时候重新部署应用程序并测试我们的新功能了。