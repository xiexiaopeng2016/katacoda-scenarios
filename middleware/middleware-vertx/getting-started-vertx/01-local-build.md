# 构建您的第一个应用程序

为了方便起见，我们使用Java编程语言和Apache Maven构建工具创建了一个基本项目。

出于教育目的，这个场景使用一个名为 ``HttpApplication.java`` 的Java类。现在打开文件，点击下面的链接:

``src/main/java/com/example/HttpApplication.java``{{open}}

当您回顾内容时，您会注意到有很多 **TODO** 注释。 **不要移除它们!** 这些注释被用作标记，没有它们，您将无法完成这个场景。

注意， ``HttpApplication`` 类继承了另一个名为 ``AbstractVerticle`` 的类。在开始实现我们的逻辑之前，让我们稍微讨论一下什么是Verticle。

# 什么是Verticle?

Verticle - Eclipse Vert.x的构建块

Vert.x在如何塑造应用程序和代码方面给了您很大的自由。但它也提供了开始编写响应式应用程序的砖块。Verticle是由Vert.x部署和运行的代码块。一个应用程序，例如微服务，通常由许多Verticle组成。Verticle通常创建服务器或客户端，注册一组处理程序，并封装系统的部分业务逻辑。

在Java中，verticle是一个扩展了verticle抽象类的类:

```java
    import io.vertx.core.AbstractVerticle;

    public class MyVerticle extends AbstractVerticle {
        @Override
        public void start() throws Exception {
            // Executed when the verticle is deployed
        }

        @Override
        public void stop() throws Exception {
            // Executed when the verticle is un-deployed
        }
    }
```

## 创建一个可以提供静态内容的简单web服务器

 **1. 编译并运行应用程序Eclipse Vert.x应用程序**

在添加代码创建web服务器之前，您应该构建并测试当前应用程序的启动情况。

首先，切换到项目目录:

``cd /root/projects/rhoar-getting-started/vertx``{{execute}}

由于这已经是一个工作的应用程序，您可以使用目标 ``vertx:run`` 的 ``maven`` 直接在本地运行它，而不需要修改任何代码

``mvn compile vertx:run``{{execute}}

>  **注意:** Vert.x maven插件在启动应用程序之前会重播执行的各个阶段，因此最好的做法是指定目标。

在这个阶段，应用程序不会做任何事情，但一段时间后，你应该会在控制台窗口中看到以下两行:

```console
[INFO] Starting vert.x application...
[INFO] THE HTTP APPLICATION HAS STARTED
```

>  **注意:**  ``"Starting vert.x application..."`` 行表示您的应用程序正在启动，并且这些顶点是异步触发的。消息 ``"THE HTTP APPLICATION HAS STARTED"`` 来自 ``System.out.println`` 在 ``HttpApplication.java`` Verticle。

 **2. 添加一个可以提供静态内容的路由器**

您的第一项工作将是添加一个可以返回HTML页面的 ``HTTP`` 服务器。

>  **注意:** 为了方便您， ``HttpApplication`` 已经有了必要的导入语句。

首先，您需要创建一个 ``Router`` 对象。这个路由器将处理所有传入的请求。在匹配的 ``TODO`` 语句所在的 ``start`` 方法 ``HttpApplication.java`` 中添加以下行(或单击将在正确位置插入代码的handy按钮)

<pre class="file" data-filename="src/main/java/com/example/HttpApplication.java" data-target="insert" data-marker="// TODO: Create a router object">Router router = Router.router(vertx);</pre>

我们还需要告诉路由器将传入的请求映射到默认位置的文件(例如 ``src/main/resources/webroot`` )。可以通过向匹配的 ``TODO`` 语句添加以下行来实现这一点。

<pre class="file" data-filename="src/main/java/com/example/HttpApplication.java" data-target="insert" data-marker="// TODO: Add a StaticHandler for accepting incoming requests">router.get("/*").handler(StaticHandler.create());</pre>

现在我们已经准备好启动HTTP服务器，

<pre class="file" data-filename="src/main/java/com/example/HttpApplication.java" data-target="insert" data-marker="// TODO: Create the HTTP server listening on port 8080">import io.vertx.core.Handler;
	import io.vertx.core.http.HttpServerRequest;

	vertx.createHttpServer().requestHandler(new Handler<HttpServerRequest>() {
		@Override
		public void handle(HttpServerRequest event) {
			router.accept(event);
		}
	}).listen(8080);
</pre>

注意:你可能已经注意到Vert.x将自动检测您的更改并立即重新部署更改。自动重新部署对于开发用途来说非常方便，但是对于生产用途可以关闭。

 **3.测试应用程序**

首先，单击该浏览器窗口的控制台框架中的 **本地网络浏览器** 选项卡，这将打开浏览器的另一个选项卡或窗口，指向客户机上的端口8080。

![Local Web Browser Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/web-browser-tab.png)

你现在应该会看到这样一个HTML页面:

![Local Web Browser Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/web-page.png)

或使用 [此](https://[[HOST_SUBDOMAIN]]-8080-[[KATACODA_HOST]].environments.katacoda.com/) 链接。

>  **注意:** Invoke按钮还不能工作，但是我们将在下一步中修复这个问题。

## 祝贺你

现在，您已经成功地执行了该场景中的第一步。

现在，您已经了解了如何仅用三行代码就可以创建一个能够使用Vert.x提供静态内容的HTTP服务器工具包。

在该场景的下一步中，我们将向应用程序中添加服务器端业务逻辑。