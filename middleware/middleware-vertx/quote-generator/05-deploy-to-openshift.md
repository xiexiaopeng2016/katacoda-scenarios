## 部署到OpenShift

现在你已经登录了OpenShift，让我们来部署我们新的微型交易Vert.x微服务:

**1. 创建一个ConfigMap**

配置映射是存储应用程序配置的Kubernetes实体。应用程序配置在src/kubernetes/config.json中。我们将从这个文件创建一个配置映射。在终端中，执行:

``oc create configmap app-config --from-file=src/kubernetes/config.json``{{execute}}

要检查配置映射是否已经正确创建，请执行:

``oc get configmap -o yaml``{{execute}}

它应该显示Kubernetes实体，并在数据输入中显示json内容。

现在已经创建了配置映射，让我们从应用程序中读取它。有几种使用配置映射的方法:

* ENV变量
* Config作为文件挂载
* Vert.x配置

我们将使用第二种方法，并将配置作为文件挂载到应用程序容器中。实际上，我们的应用程序已经配置为从src/kubernetes/config.json文件中读取配置:

```java
private ConfigRetrieverOptions getConfigurationOptions() {
    JsonObject path = new JsonObject().put("path", "src/kubernetes/config.json");
    return new ConfigRetrieverOptions().addStore(new ConfigStoreOptions().setType("file").setConfig(path));
}
```

为此，我们在``quote-generator/src/main/fabric8/deployment.yml``{{open}}中定义了额外的配置，其中包含了正确的配置:

1. 使用配置映射内容定义卷
2. 将这个卷挂载到正确的目录中

您还可以看到，该文件包含我们传递给进程的JAVA选项。

**2. 启动报价生成器**

Red Hat OpenShift应用程序运行时包括一个强大的maven插件，可以使用现有的Eclipse Vert.x应用程序，并生成必要的Kubernetes配置。

使用以下命令构建和部署项目，这将使用maven插件来部署:

``mvn fabric8:deploy``{{execute}}

构建和部署可能需要一到两分钟。等待它完成。您应该看到构建结束时输出的一个**BUILD SUCCESS**。

maven构建完成后，应用程序将在不到一分钟的时间内变得可用。
要验证一切都已启动，运行以下命令，并等待它成功完成:

``oc rollout status -w dc/quote-generator``{{execute}}

**3.访问在OpenShift上运行的应用程序**

点击 [路由的URL](http://quote-generator-vertx-kubernetes-workshop.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com) 
访问示例UI。

> 还可以通过OpenShift Web控制台概述页面上的quote-generator路由链接访问应用程序。

你现在应该会看到这样一个HTML页面:

```json

{
  "MacroHard" : {
    "volume" : 100000,
    "shares" : 51351,
    "symbol" : "MCH",
    "name" : "MacroHard",
    "ask" : 655.0,
    "bid" : 666.0,
    "open" : 600.0
  },
  "Black Coat" : {
    "volume" : 90000,
    "shares" : 45889,
    "symbol" : "BCT",
    "name" : "Black Coat",
    "ask" : 654.0,
    "bid" : 641.0,
    "open" : 300.0
  },
  "Divinator" : {
    "volume" : 500000,
    "shares" : 251415,
    "symbol" : "DVN",
    "name" : "Divinator",
    "ask" : 877.0,
    "bid" : 868.0,
    "open" : 800.0
  }
}
```

**4. 构建和部署微型交易仪表板**

``cd /root/code/micro-trader-dashboard``{{execute}}

``mvn fabric8:deploy``{{execute}}

在OpenShift web控制台中，等待pod就绪，然后单击关联的路由。在URL的末尾添加"/admin"，您应该看到仪表板。如果你进入交易者选项卡，图表应该显示市场的演变。

或者，您可以单击
 [路由的URL](http://micro-trader-dashboard-vertx-kubernetes-workshop.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/admin) 
访问示例UI。

**5. 你不是金融专家?**
也许你不习惯金融世界和词汇，我也不习惯，这是一个过于简化的版本。让我们定义重要的字段:

*  ``name`` :公司名称

*  ``symbol`` :短名称

*  ``shares`` :可以购买的股票数量

*  ``open`` :交易日开盘时的股价

*  ``ask`` :你买股票时的价格(卖价)

*  ``bid`` :你卖出股票时的价格(买入价)


你可以查看维基百科了解更多细节。

## 恭喜你!

您已经将报价生成器部署为一个微服务。在下一个组件中，我们将实现一个事件总线服务(portfolio微服务)。