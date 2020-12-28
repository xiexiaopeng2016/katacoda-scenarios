# 使用服务器端逻辑扩展应用程序

在第1步中，您学习了如何启动HTTP服务器，并使用静态处理程序来服务器静态文件，如HTML、CSS等。在这一步中，我们将创建一个使用服务器端代码的新处理程序。

仔细看看``src/main/resources/webroot/index.html``{{open}}，我们可以看到在末尾有一个JavaScript函数，当有人点击 ``Invoke`` 按钮时，它应该做出反应。从 ``$.getJSON("/api/greeting?name="`` 行我们可以看到，网页期待一个API调用，它将充当问候函数。其思想是，API函数应该获取输入字段的值，并将其转换为问候字符串。

**1. 添加处理问候电话的方法**

首先，我们将实现一个称为greeting的路由处理程序。您将实现它作为 ``HttpApplication`` 类中的一个私有方法，该方法以 ``RoutingContext`` 作为参数。

首先再次打开``src/main/java/com/example/HttpApplication.java``{{open}}。

首先复制并粘贴下面 ``// TODO: Add method for greeting here`` 行的代码。

<pre class="file" data-filename="src/main/java/com/example/HttpApplication.java" data-target="insert" data-marker="// TODO: Add method for greeting here">private void greeting(RoutingContext rc) {
    String name = rc.request().getParam("name");
    if (name == null) {
        name = "World";
    }

    JsonObject response = new JsonObject()
        .put("content", String.format(template, name));

    rc.response()
        .putHeader(CONTENT_TYPE, "application/json; charset=utf-8")
        .end(response.encodePrettily());
    }
</pre>

该方法使用名为 ``template`` 的成员变量，目前定义为 ``static final String template = "Hello, %s!";`` 。

注意:因为我们希望处理程序立即向浏览器返回响应，所以我们将使用 ``rc.response().end()`` 。但是，可以使用a399b和 ``rc.next()`` 来链接几个处理程序。

**2.添加一个路线**

在实现了这个处理程序之后，我们现在需要像这样添加一个匹配 ``/api/greeting`` 的路由:

<pre class="file" data-filename="src/main/java/com/example/HttpApplication.java" data-target="insert" data-marker="// TODO: Add router for /api/greeting here">router.get("/api/greeting").handler(this::greeting);</pre>

注意:最好的做法是在通配符路由之前添加更多特定的路由。x将按照添加时的顺序遍历路由器，如果找到匹配的路由并调用 ``rc.end()`` ，则不会执行后续的路由。

**3.测试应用程序**

现在您应该能够 [在这里](https://[[HOST_SUBDOMAIN]]-8080-[[KATACODA_HOST]].environments.katacoda.com/) 使用 **调用** 按钮了。通过在输入中添加不同的值进行测试，也可以通过更改 ``HttpApplication.java`` 中的 ``template`` 字符串进行测试，以使用另一种语言。

**4. 停止应用程序**

在继续之前，单击终端窗口，然后按 **ctrl-c** 停止运行的应用程序!

## 祝贺你

现在，您已经学习了如何使用多个路由以及如何实现返回JSON的HTTP服务调用。

在这个场景的下一步中，我们将把我们的应用程序部署到OpenShift容器平台。