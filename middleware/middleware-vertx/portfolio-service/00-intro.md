## 事件总线服务——投资组合服务

在这个场景中，我们将实现一个事件总线服务。一个 ``Portfolio`` 储存拥有的股份和可用的现金。

**1. 初始化katacoda环境**

这个实验室中的所有场景都是连续的，并且是建立在彼此的基础上的。在此场景中开发的投资组合微服务依赖于quote generator微服务，该微服务应该已经在OpenShift容器平台上构建并运行了。这就是在终端中运行的脚本所做的事情。它是:

1. 克隆源代码
2. 初始化OpenShift环境
3. 构建和部署报价生成器场景
4. 构建和部署微型交易员仪表板

**2. 简介- RPC和异步RPC**

微服务不仅仅是关于REST的。它们可以使用任何类型的交互来公开，远程过程调用就是其中之一。使用RPC，组件可以通过执行本地过程调用有效地将请求发送到另一个组件，这将导致将请求打包到消息中并发送给被调用方。同样，结果被发送回，并作为过程调用的结果返回到调用方组件:

![Architecture](/openshift/assets/middleware/rhoar-getting-started-vertx/rpc-sequence.png)

这种交互具有引入类型化的优点，因此比非结构化消息更不易出错。然而，它也在调用者和被调用者之间引入了更紧密的耦合。调用者知道如何调用被调用者:

1. 如何调用服务
2. 服务所在地点(地点)

![Architecture](/openshift/assets/middleware/rhoar-getting-started-vertx/async-rpc-sequence.png)

AsyncResult通知处理程序调用是成功还是失败。成功后，处理程序就可以检索结果。

这样的async-RPC有几个优点:

* 调用者没有被阻塞
* 它处理失败
* 它避免您在事件总线上发送消息，并为您管理对象编组和解组。