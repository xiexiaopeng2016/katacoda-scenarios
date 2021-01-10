## 实施服务

现在是实现异步服务接口的时候了。我们将在这个服务中实现三个方法:

* ``getPortfolio`` 了解如何创建AsyncResult对象

* ``sendActionOnTheEventBus`` 查看如何在事件总线上发送消息

* ``evaluate`` 计算投资组合的当前价值

**1. 创建AsyncResult实例**

正如我们在上面看到的，我们的异步服务有一个 ``Handler<AsyncResult<Portfolio>>`` 参数。因此，当我们实现这个服务时，我们需要使用 ``AsyncResult`` 的实例调用 ``Handler`` 。为了了解它是如何工作的，让我们实现 ``getPortfolio`` 方法:

在 ``io.vertx.workshop.portfolio.impl.PortfolioServiceImpl`` 中，填写 ``getPortfolio`` 方法。它应该调用 ``resultHandler`` 的 ``handle`` 方法，并获得成功的异步结果。这个对象可以通过(Vert.x) ``Future`` 方法创建。

在编辑器中打开文件:

``portfolio-service/src/main/java/io/vertx/workshop/portfolio/impl/PortfolioServiceImpl.java``{{open}}

然后，将下面的内容复制到匹配的 ``// TODO: getPortfolio`` 语句中(或使用 ``Copy to Editor`` 按钮):

<pre class="file" data-filename="portfolio-service/src/main/java/io/vertx/workshop/portfolio/impl/PortfolioServiceImpl.java" data-target="insert" data-marker="// TODO: getPortfolio">
resultHandler.handle(Future.succeededFuture(portfolio));
</pre>

让我们仔细分析它:

* resultHandler.handle : 这将调用处理程序。Handler<X>只有一个方法(handle(X))。
* Future.succeededFuture : 这就是我们如何创建一个表示成功的AsyncResult实例。传递的值是结果(投资组合)

 ``AsyncResult`` 和 ``Future`` 是什么关系? 一个 ``Future`` 表示一个可能发生，也可能没有发生的行为的结果。如果使用 ``Future`` 来检测操作是否完成，则结果可能为null。 ``Future`` 对象背后的操作可能成功，也可能失败。``AsyncResult`` 是一个描述操作失败成功的结构。所以 ``Future`` 就是 ``AsyncResult`` 。在Vert.x中 ``AsyncResult`` 实例是从 ``Future`` 类创建的。

``AsyncResult`` 描述:

* 一个成功，如前所示的，它封装了结果
* 一个失败，它封装了一个``Throwable``实例

那么，这是如何与我们的异步RPC服务一起工作的，让我们看看这个序列图:

![Architecture](/openshift/assets/middleware/rhoar-getting-started-vertx/portfolio-sequence.png)

**2. 在事件总线上发送事件**
现在该看看如何在事件总线上发送消息了。您可以使用vertx.eventBus()访问事件总线。从这个对象你可以:

* ``send`` : 以点对点模式发送一个消息
* ``publish`` : 向在该地址上注册的所有消费者广播一条消息
* ``send``与一个``Handler<AsyncResult<Message>>>`` : 以点对点模式发送消息并期待回复。如果使用RX Java，则调用此方法``rxSend``并返回一个``Single<Message>``。如果接收方没有回复消息，则视为失败(超时)

在我们的代码中，我们提供了 ``buy`` 和 ``sell`` 方法，它们只是在买卖股票之前做一些检查。动作发出后，我们在事件总线上发送一条消息，该消息将被 ``Audit Service`` 和 ``Dashboard`` 使用。所以, 我们会用 ``publish`` 方法。

编写 ``sendActionOnTheEventBus`` 方法的主体，以便在包含 ``JsonObject`` 主体的 ``EVENT_ADDRESS`` 地址上发布消息。该节点必须包含以下条目:

* action → 动作(买或卖)
* quote → 报价为Json
* date → 一个日期(单位为毫秒)
* amount → 金额
* owned → 已更新的(现有)金额

将下面的代码复制到匹配的 ``// TODO: sendActionOnTheEventBus`` 语句中

<pre class="file" data-filename="portfolio-service/src/main/java/io/vertx/workshop/portfolio/impl/PortfolioServiceImpl.java" data-target="insert" data-marker="// TODO: sendActionOnTheEventBus">
vertx.eventBus().publish(EVENT_ADDRESS, new JsonObject()
    .put("action", action)
    .put("quote", quote)
    .put("date", System.currentTimeMillis())
    .put("amount", amount)
    .put("owned", newAmount));
</pre>

让我们来深入了解一下:

* 它得到了``EventBus``实例, 并在上面调用``publish``。第一个参数是发送消息的地址
* 主体是一个``JsonObject``包含不同的操作信息(买或卖，报价(另一个json对象)，日期…

**3.协调异步方法和消费HTTP端点 - 组合价值评估**

最后实现的方法是 ``evaluate`` 方法。这种方法计算投资组合的当前价值。然而，为此它需要访问"current"股票的价值(最后的报价)。它将使用我们在报价生成器中实现的HTTP端点。为此，我们要:

* 发现服务
* 为每个我们拥有一些股份的公司调用服务
* 当所有调用都完成后，计算值并将其发送回调用者

让我们一步一步来做。首先，在评估中，我们需要检索报价生成器提供的HTTP端点(服务)。该服务名为quotes。我们在上一节中发表过。所以，让我们开始得到这个服务。

填写evaluate方法以检索quotes服务。您可以使用HttpEndpoint.getClient检索Http服务。服务的名称是quotes。如果无法检索服务，只需将一个失败的异步结果传递给处理程序。否则, computeEvaluation打电话。

将以下内容复制到evaluate方法中匹配的 ``// TODO: evaluate`` 语句中

<pre class="file" data-filename="portfolio-service/src/main/java/io/vertx/workshop/portfolio/impl/PortfolioServiceImpl.java" data-target="insert" data-marker="// TODO: evaluate">
quotes.subscribe((client, err) -> {
 if (err != null) {
     resultHandler.handle(Future.failedFuture(err));
 } else {
     computeEvaluation(client, resultHandler);
 }
});
</pre>

* 获取请求的服务的HTTP客户机。
* 无法检索客户端(未找到服务)，报告失败
* 我们有了客户端，我们继续…

下面是如何实现 ``computeEvaluation`` 方法:

```java
private void computeEvaluation(HttpClient httpClient, Handler<AsyncResult<Double>> resultHandler) {
    // We need to call the service for each company we own shares
    List<Future> results = portfolio.getShares().entrySet().stream()
        .map(entry -> getValueForCompany(httpClient, entry.getKey(), entry.getValue()))    
        .collect(Collectors.toList());


    // We need to return only when we have all results, for this we create a composite future.
    // The set handler is called when all the futures has been assigned.
    CompositeFuture.all(results).setHandler(                                            
      ar -> {
        double sum = results.stream().mapToDouble(fut -> (double) fut.result()).sum();  
        resultHandler.handle(Future.succeededFuture(sum));                              
    });
}
```

现在，我们只需要调用该服务的 ``getValueForCompany`` 方法。编写此方法的内容。

这个方法返回一个Single<Double>，发出 numberOfShares * bid 结果。按照以下步骤编写该方法的内容:

1. 使用 client.get("/?name=" + encode(company)) 创建HTTP请求
2. 我们期望一个JSON对象作为响应负载，所以使用 .as(BodyCodec.jsonObject())
3. 使用rxSend方法创建一个包含结果的单个对象
4. 我们现在需要从返回的JSON中提取"bid"。提取响应主体，然后提取"bid"条目(json.getDouble("bid"))。这两种提取都使用map进行编排。
5. 计算金额 (bid * numberOfShared)
6. 完成!

将以下内容复制到getValueForCompany方法中匹配的 ``// TODO: getValueForCompany`` 语句中

<pre class="file" data-filename="portfolio-service/src/main/java/io/vertx/workshop/portfolio/impl/PortfolioServiceImpl.java" data-target="insert" data-marker="// TODO: getValueForCompany">
 return client.get("/?name=" + encode(company))
     .as(BodyCodec.jsonObject())
     .rxSend()
     .map(HttpResponse::body)
     .map(json -> json.getDouble("bid"))
     .map(val -> val * numberOfShares);                              
</pre>