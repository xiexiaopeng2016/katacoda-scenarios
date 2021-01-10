## 部署到OpenShift

现在你已经登录了OpenShift，让我们来部署我们新的微型交易员Vert.x微服务:

**1. 构建和部署**

我们已经在OpenShift上部署了我们的 ``quote-generator`` 和 ``micro-trader-dashboard`` 微服务。在这一步中，我们将部署我们的新投资组合微服务。我们将继续使用相同的OpenShift项目来容纳这个服务和其他微服务。

``oc project vertx-kubernetes-workshop``{{execute}}

如你所知，Red Hat OpenShift应用程序运行时包括一个强大的maven插件，它可以使用现有的Eclipse Vert.x应用程序，并生成必要的Kubernetes配置。

使用以下命令构建和部署项目，这将使用maven插件来部署:

``cd /root/code/portfolio-service``{{execute}}

``mvn fabric8:deploy``{{execute}}

构建和部署可能需要一到两分钟。等待它完成。您应该看到构建结束时输出的一个**BUILD SUCCESS**。

maven构建完成后，应用程序将在不到一分钟的时间内变得可用。
要验证一切都已启动，运行以下命令，并等待它成功完成:

``oc rollout status -w dc/portfolio-service``{{execute}}

这样，portfolio服务就启动了。它发现 ``quotes`` 服务并准备好使用。

**2. 访问微型交易仪表板**

点击"本地网络浏览器"选项卡旁边的"OpenShift控制台"选项卡。

![OpenShift Console Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/openshift-console-tab.png)

用户名和密码使用 ``developer/developer`` 登录。您应该看到新创建的名为 ``"vertx-kubernetes-workshop"`` 的项目。点击它。您应该看到四个正在运行的pod，一个用于前面场景中创建的quote-generator和micro-trader-dashboard微服务，另一个用于刚刚创建的portfolio-service。

点击 ``micro-trader-dashboard`` 的路由。在路由的末尾添加 ``“/admin”`` ，您应该会看到仪表板。你应该会看到一些新的服务，如果你点击左侧的“Trader”标签，现金应该已经设置在左上角。

或者，您可以单击 [路由的URL](http://micro-trader-dashboard-vertx-kubernetes-workshop.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/admin) 访问仪表板。

指示板使用异步RPC机制消费组合服务。JavaScript的客户机是在编译时生成的，并使用SockJS进行通信。在引擎盖背后，在事件总线和SockJS之间有一座桥。

## 恭喜你!

您已经部署了运行在OpenShift上的投资组合微服务。在下一个组件中，我们将实现trader服务并使用它来买卖股票。