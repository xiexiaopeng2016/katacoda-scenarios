在这个场景中，您将使用 [Eclipse Vert.x](https://vertx.io) 了解更多关于响应式微服务的信息, [Red Hat OpenShift应用程序运行时](https://developers.redhat.com/products/rhoar) 中包含的一个运行时。

这个场景是一系列场景中的第一个，这些场景将带领您使用Vert.x构建一个响应式应用程序。说明Vert.x是什么。这些场景为Vert.x提供了一个中间的、实际操作的会话。从第一行代码，到生产服务，再到消费服务，最后到在一个一致的响应式系统中组装一切。它说明了什么是响应式系统，什么是响应式编程，以及如何构建基于响应式微服务的应用程序。

## Micro-Trader应用程序

正在开发的Vert.x应用程序称为 ``Micro-Trader`` ，由如下所示的多个微服务组成。这是一个虚拟的金融应用，我们将在其中赚(虚拟的)钱。该应用程序由以下微服务组成:

* quote generator - 这是一个绝对不现实的模拟器，为3个虚构的公司MacroHard, Divinator和Black Coat生成报价。市场数据发布在Vert.x事件总线上。它还发布一个HTTP端点来获取报价的当前值。
* traders - 这是一组从报价生成器接收报价并决定是否购买或出售特定股票的组件。为了做出这个决定，它们依赖于另一个称为portfolio服务的组件。
* portfolio - 这项服务管理我们投资组合中的股票数量及其货币价值。它被公开为一个服务代理，即在Vert.x事件总线之上的异步RPC服务。对于每一个成功的操作，它都会在事件总线上发送一条描述操作的消息。它使用报价生成器来评估投资组合的当前价值。
* audit - 这是为了记录我们所有的操作(是的，这是法律规定的)。审计组件通过事件总线和地址从portfolio服务接收操作。并存储在数据库中。它还提供了一个REST端点来检索最新的操作集。
* dashboard - 一些用户界面，当我们变得富有时, 让我们知道。

让我们来看看架构:

![Architecture](/openshift/assets/middleware/rhoar-getting-started-vertx/reactive-ms-architecture.png)

该应用程序使用几种类型的服务:

* HTTP端点(即REST API) - 这个服务使用HTTP URL定位。
* gRPC - gRPC是建立在HTTP/2之上的一个安全、快速的RPC框架
* 消息源 - 这些是在事件总线上发布消息的组件，服务使用(事件总线)地址定位。

所有组件都将部署在同一个Kubernetes名称空间(项目)中，并形成一个集群。

仪表板显示可用的服务、每个公司报价的价值、交易者的最新操作集和投资组合的当前状态。它还显示不同的断路器的状态。

![Architecture](/openshift/assets/middleware/rhoar-getting-started-vertx/dashboard.png)

## 第一个微服务 - 报价生成器

在这个场景中，您将创建第一个微服务 - quote生成器。在接下来的每个场景中，您将创建一个微服务(从上面的集合中创建)，它将共同构成基于Vert.x的微交易应用程序。