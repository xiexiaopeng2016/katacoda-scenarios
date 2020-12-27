这个示例项目展示了使用Node.js和NPM最佳实践的Node.js项目的组件。

该应用程序实现了一个简单的RESTful微服务，它实现了一个问候服务(它只返回一个
Hello 问候)。

 **1. 检查应用程序代码**

点击下面的链接打开每个文件并查看其内容:

* ``package.json``{{open}} - 项目的元数据: 名称、版本、依赖项以及构建和维护项目所需的其他信息。
* ``app.js``{{open}} - 示例应用程序的主要逻辑，定义REST端点和应用程序运行时配置。
* ``app-config.yml``{{open}} - 最初用于填充OpenShift ConfigMap的内容，示例应用程序将在运行时访问该ConfigMap。
* ``public/index.html``{{open}} - 访问问候服务的简单web UI。

稍微检查一下内容，注意代码中有一些 ``TODO`` 注释。不要移除它们! 注释被用作标记，如果没有它们，您将无法完成该场景。

在 ``app.js`` 中定义的 ``/api/greeting`` API返回一个简单的消息，其中包括一个可选的名称。稍后您将修改此文件。

 **2. 安装依赖关系**

依赖项列在 ``package.json`` 文件中，并声明这个示例应用程序需要哪些外部项目。
要下载并安装它们，运行以下命令:

``npm install``{{execute HOST1}}

> 您可以单击上面的命令(以及本场景中的所有其他命令)，自动将其复制到终端并执行

下载它需要几秒钟的时间，您应该会看到像 ``added 774 packages in 9.79s`` 这样的最终报告。

 **3. 运行应用程序**

在向项目添加代码之前，您应该构建并测试当前应用程序的启动情况。

因为这是一个工作的应用程序，使用 ``npm`` 在本地运行应用程序:

``npm start``{{execute HOST1}}

在这一阶段，应用程序不会真正做任何事情，但一段时间后，你会看到:

```console
> nodejs-configmap@1.0.0 start /root/projects/rhoar-getting-started/nodejs
> node .
```

 **3. 测试应用程序**

首先，单击此浏览器窗口的控制台框架中的 **本地的网络浏览器** 选项卡。这将打开浏览器的另一个选项卡或窗口，指向客户端的端口8080。

![Local Web Browser Tab](/openshift/assets/middleware/rhoar-getting-started-nodejs/web-browser-tab.png)

您现在应该看到如下所示的html页面

![App](/openshift/assets/middleware/rhoar-getting-started-nodejs/app.png)

这表明应用程序已正确启动。在name字段中输入您的名字并单击 **调用** 。默认的
返回硬编码的问候。

![Hardcode](/openshift/assets/middleware/rhoar-getting-started-nodejs/hardcode.png)

 **4. 停止应用程序**

在继续之前，单击终端窗口，然后按CTRL-C停止运行的应用程序!

## 祝贺你

现在，您已经成功地执行了该场景中的第一步。

现在，您已经了解了如何用几行代码创建一个简单的RESTful HTTP服务器，它能够使用Node.js提供静态内容。

在这个场景的下一步中，我们将把我们的应用程序部署到OpenShift容器平台。