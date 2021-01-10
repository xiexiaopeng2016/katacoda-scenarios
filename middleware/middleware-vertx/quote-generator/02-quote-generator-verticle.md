## 垂直

正如你可能已经注意到的，代码的结构是3 ``verticles`` ，但这些是什么?立交是一种构造立交的方式。x应用程序代码。这不是强制性的，但是很方便。垂直是部署在垂直顶点上的一段代码。x实例。一个垂直对象可以访问它所部署的 ``vertx`` 的实例，并且可以部署其他垂直对象。

**理解应用程序**

让我们通过点击下面的链接打开 ``GeneratorConfigVerticle`` 类，并查看 ``start`` 方法

``quote-generator/src/main/java/io/vertx/workshop/quote/GeneratorConfigVerticle.java``{{开放}}

此方法检索配置、实例化顶点并在服务发现中发布服务。

首先，请注意方法签名。它接收一个Future对象，该对象指示启动是异步的。实际上，在这个方法中进行的所有操作都是异步的。因此，当调用方线程到达方法的末尾时，操作可能还没有完成。我们使用给定的Future来指示流程何时完成(或失败)。

启动方法:

1. 获取配置(给出“伪造”);公司设置)
2. 每个定义的连部署一个垂直
3. 部署RestQuoteAPIVerticle
4. 公开市场数据信息来源
5. 通知给定的Future成功完成或失败

当您回顾内容时，您会注意到有2个TODO注释。不要移除它们!这些注释被用作标记，没有它们，您将无法完成这个场景。

要检索配置，垂直需要 ``ConfigRetriever`` 。这个对象允许从不同的存储(如git、文件、http等)检索配置块。这里我们只加载位于src/kubernetes目录中的 ``config.json`` 文件的内容。配置是一个JsonObject。绿色。x大量使用JSON，所以在这个实验中你会看到很多JSON。

一旦我们有了检索器，我们就可以检索配置。这是一个异步方法( ``rxGetConfig`` )，返回一个单独的(包含一个项目的流)。在获取配置之后，我们从其中提取companies数组，并为每个定义的公司部署一个垂直。该部署也是异步的，使用 ``rxDeployVerticle`` 完成。这些公司立柱模拟股票的价值。报价在市场地址的事件总线上发送。

将以下内容添加到匹配的 ``// TODO: MarketDataVerticle`` 语句中(或使用 ``Copy to Editor`` 按钮):

<pre class="file" data-filename="src/main/java/io/vertx/workshop/quote/GeneratorConfigVerticle.java" data-target="insert" data-marker="// TODO: MarketDataVerticle">
.flatMapSingle(company -> vertx.rxDeployVerticle(MarketDataVerticle.class.getName(),
    new DeploymentOptions().setConfig(company)))
</pre>

在部署了公司的垂直节点之后，我们将部署另一个提供HTTP API来访问市场数据的垂直节点。

将以下内容添加到匹配的 ``// TODO: RestQuoteAPIVerticle`` 语句(或使用 ``Copy to Editor`` 按钮):

<pre class="file" data-filename="quote-generator/src/main/java/io/vertx/workshop/quote/GeneratorConfigVerticle.java" data-target="insert" data-marker="// TODO: RestQuoteAPIVerticle">
.flatMap(l -> vertx.rxDeployVerticle(RestQuoteAPIVerticle.class.getName()))
</pre>

方法的最后一部分是关于微服务一节中提到的服务发现。该组件生成在事件总线上发送的报价。但是为了让其他组件发现消息被发送到哪里(哪里意味着在哪个地址上)，它注册了它。 ``market-data`` 是服务的名称， ``ADDRESS`` (定义为market的静态最终变量)是发送消息的事件总线地址。

```java
.flatMap(x -> discovery.rxPublish(MessageSource.createRecord("market-data", ADDRESS)))
```

最后，当一切都完成后，我们报告给定Future对象的状态。故障管理可以在任何阶段进行，但通常是在subscribe方法中完成的:

```java
object.rxAsync(param1, param2)
 // ....
 .subscribe((rec, err) -> {
     if (rec != null) {
         future.complete();
     } else {
         future.fail(err);
     }
 });
```

如果您还记得这个体系结构，报价生成器还提供一个HTTP端点，返回报价的最后值。注意，该服务在服务发现中没有显式发布。这是因为Kubernetes负责这部分。绿色。x服务发现与Kubernetes服务交互，所以所有Kubernetes服务都可以通过Vert.x检索