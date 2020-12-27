代码和ConfigMap就绪后，让我们使用与前面相同的命令重新构建和重新部署。执行命令:

``npm run openshift``{{execute}}

重新构建和重新部署可能需要一到两分钟。等待它完成。

构建完成后，应用程序将在不到一分钟的时间内变得可用。
要验证一切都已启动，再次运行以下命令

``oc rollout status dc/nodejs-configmap``{{execute}}

然后等待它报告
 ``replication controller "nodejs-configmap-2" successfully rolled out``

重新部署应用程序后，通过单击 [应用程序链接](http://nodejs-configmap-example.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com) 重新访问示例UI

> 您还可以通过OpenShift Web控制台概述页面上的链接访问该应用程序。![Overview link](/openshift/assets/middleware/rhoar-getting-started-nodejs/overview-link.png)

应用程序现在将读取ConfigMap值，并使用它们来代替硬编码的默认值。

 **测试更新后的应用程序**

在'Name'字段，并单击 **调用** 以测试服务。你应该现在看到更新的消息 ``Hello, [name] from a ConfigMap !`` ，它指示应用程序成功访问了ConfigMap并将其值用于消息。

![New message](/openshift/assets/middleware/rhoar-getting-started-nodejs/new-message.png)

在最后一步中，我们将修改ConfigMap并验证应用程序是否成功自动获取更改。