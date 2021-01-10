## 引用REST端点

打开 ``RestQuoteAPIVerticle`` 。这个verticle公开了一个HTTP端点来检索maker数据的当前/最近的值(报价)。在 ``start`` 方法中，需要:

* 接收事件总线行情消息以收集最后的报价(在``quotes``映射)
* 处理HTTP请求，以返回报价列表或一个单独的报价，如果设置了``name``(查询)参数。

在这个例子中，我们使用的是流(Flowable)。流是响应式编程和体系结构的重要组成部分。

我们就这么做吧……

**1. 实现接收事件的处理程序**

第一个行动是观察市场信息流。这是使用 ``vertx.eventBus().<JsonObject>consumer(GeneratorConfigVerticle.ADDRESS).toFlowable()`` 完成的。现在我们有了消息流，但是我们需要提取JSON主体并填充quotes映射。实现提取消息主体的缺失逻辑(使用 ``body()`` 方法)，然后将 ``name → quote`` 放入 ``quotes`` 映射中。

在编辑器中打开文件:

``quote-generator/src/main/java/io/vertx/workshop/quote/RestQuoteAPIVerticle.java``{{open}}

然后，将下面的内容复制到匹配的 ``// TODO`` 语句中(或使用 ``Copy to Editor`` 按钮):

使用 ``.map(msg -> {})`` 提取消息主体

<pre class="file" data-filename="quote-generator/src/main/java/io/vertx/workshop/quote/RestQuoteAPIVerticle.java" data-target="insert" data-marker="// TODO: Extract the body of the message">
.map(Message::body)  
</pre>

对于每个消息，用接收到的报价填充 ``quotes`` 映射。使用 ``.doOnNext(json -> {})``
报价是可以从消息体中检索的json对象。该映射的结构如下: name -> quote

<pre class="file" data-filename="quote-generator/src/main/java/io/vertx/workshop/quote/RestQuoteAPIVerticle.java" data-target="insert" data-marker="// TODO: For each message, populate the quotes map with the received quote.">
.doOnNext(json -> {
    quotes.put(json.getString("name"), json); // 2
})
</pre>

**2. 实现处理程序来处理HTTP请求**

现在您已经有了 ``quotes`` ，让我们使用它们来处理HTTP请求。代码已经创建了HTTP服务器并提供了HTTP请求流。流为服务器接收到的每个HTTP请求发出一个项。因此，您需要处理请求并编写响应。

编写请求处理程序的内容以响应请求:

1. 一个将content-type头设置为 ``application/json`` 的响应(已经完成)
2. 检索``name``参数(这是公司名称)
3. 如果没有设置公司名称，则将以json返回所有报价。

如果设置了公司名称，则返回存储的报价，如果公司未知则返回404响应
将以下内容复制到匹配的 ``// TODO: Handle the HTTP request`` 语句中

<pre class="file" data-filename="quote-generator/src/main/java/io/vertx/workshop/quote/RestQuoteAPIVerticle.java" data-target="insert" data-marker="// TODO: Handle the HTTP request">
String company = request.getParam("name");
if (company == null) {
    String content = Json.encodePrettily(quotes);
    response.end(content);
} else {
    JsonObject quote = quotes.get(company);
    if (quote == null) {
        response.setStatusCode(404).end();
    } else {
        response.end(quote.encodePrettily());
    }
}
</pre>

1. 从请求中获取响应对象
2. 获取name参数(查询参数)
3. 将映射编码为JSON
4. 写入响应并使用end(…)刷新响应
5. 如果给定的name与公司不匹配，则将状态码设置为404

您可能想知道为什么不需要同步。实际上，我们无需任何同步构造就可以在映射中写入和读取。下面是Vert.x的一个主要特性:所有这些代码都将由相同的事件循环执行，因此总是由相同的线程访问，永远不会并发。

你已经看过Vert.x开发的基本原理了，包括异步API和AsyncResult，实现处理程序并从事件总线接收消息

在这个场景的下一步中，我们将把我们的应用程序部署到OpenShift容器平台。