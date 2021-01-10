## 异步服务接口

要创建一个异步RPC服务或事件总线服务或服务代理，您首先需要一个Java接口来声明异步方法。

点击链接打开 ``io.vertx.workshop.portfolio.PortfolioService`` 类:

``portfolio-service/src/main/java/io/vertx/workshop/portfolio/PortfolioService.java``{{open}}

这个类被注释为:

* ``ProxyGen`` - 启用事件总线服务代理和服务器生成

* ``VertxGen`` - 启用用Vert.x支持的不同语言创建代理

让我们来看看第一种方法:

```java
void getPortfolio(Handler<AsyncResult<Portfolio>> resultHandler);
```

这个方法允许您检索一个Portfolio对象。该方法是异步的，因此有一个接收AsyncResult<Portfolio>的处理程序参数。其他方法遵循同样的模式。

**请注意**
您可能还注意到包有一个package-info.java文件。此文件是启用服务代理生成所需的文件。