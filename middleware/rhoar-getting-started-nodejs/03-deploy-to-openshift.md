现在您已经登录到OpenShift，让我们部署与前面相同的示例应用程序。

 **1. 构建和部署**

使用以下命令构建和部署项目:

``npm run openshift``{{execute}}

它使用NPM和 [Nodeshift](https://github.com/bucharest-gold/nodeshift) 项目来构建和部署示例应用程序到OpenShift，使用容器化的Node.js运行时。Nodeshift使用示例项目的 ``.nodeshift`` 目录中的文件，以创建必要的Kubernetes对象，以便部署应用程序。

构建和部署可能需要一到两分钟。等待它完成。您应该在构建输出的末尾看到 ``INFO complete`` ，而您不应该看到任何明显的错误或失败。

构建完成后，应用程序将在不到一分钟的时间内变得可用。
要验证一切都已启动，请运行以下命令

``oc rollout status dc/nodejs-configmap``{{execute}}

你会看到
 ``replication controller "nodejs-configmap-1" successfully rolled out``

 **2. 访问在OpenShift上运行的应用程序**

这个示例项目包括一个简单的UI，它允许您访问Greeting API。单击路由URL以在单独的浏览器选项卡中打开示例应用程序:

> 您还可以通过OpenShift Web控制台概述页面上的链接访问该应用程序。![Overview link](/openshift/assets/middleware/rhoar-getting-started-nodejs/overview-link.png)

在'Name'字段，并单击 **调用** 以测试服务。您应该得到相同的硬编码，如前面步骤所示。

![Hardcoded message](/openshift/assets/middleware/rhoar-getting-started-nodejs/hardcode.png)

虽然问候代码是可用的，但如果您想更改消息，则需要停止应用程序，更改代码，然后重新部署。在下一节中，您将在现实世界中了解到这一点这可能不可行，需要一种动态更改内容的机制。
您将使用OpenShift  _ConfigMaps_ 添加这个。