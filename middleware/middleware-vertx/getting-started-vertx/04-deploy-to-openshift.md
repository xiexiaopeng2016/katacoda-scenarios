# 部署到OpenShift

在本地计算机上运行应用程序对于快速运行非常有用，但是在类似于产品的环境中测试应用程序也很好。

注意: **Openshift** 还提供了很棒的CI/CD和管道功能，但这超出了入门场景的范围。

**1. 将应用程序部署到您的私有项目**

Red Hat OpenShift应用程序运行时包含了一个强大的maven插件，可以使用现有的Vert.x应用程序，并生成必要的Kubernetes配置。

要部署我们的应用程序(和路由)，只需执行以下操作

``mvn fabric8:deploy -Popenshift``{{execute}}

**2. 验证**

maven构建完成后，通常只需不到20秒的时间应用程序就可用了。要验证一切都已启动，运行以下命令，并等待它报告 ``replication controller "http-vertx-1" successfully rolled out`` :

``oc rollout status dc/http-vertx``{{execute}}

然后去openshift web控制台，点击路由或 [这里](http://http-vertx-dev.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com)

测试并验证Invoke按钮是否正常工作。

## 祝贺你

现在，您已经成功地将应用程序部署到OpenShift容器平台。

现在，您已经了解了如何将现有的应用程序部署到OpenShift/Kubernetes。