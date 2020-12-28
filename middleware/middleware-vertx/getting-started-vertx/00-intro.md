在这个场景中，您将了解更多关于Eclipse Vert的信息, [Red Hat OpenShift应用程序运行时](https://developers.redhat.com/products/rhoar) 中包含的一个运行时。

## 你会学到什么

您将学习如何开始构建一个响应式web应用程序，该应用程序可以使用Eclipse Vert.x提供静态内容和服务器端业务逻辑。

## 什么是Eclipse Vert.x?

![Local Web Browser Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/vertx-logo.png)

Eclipse Vert.x是一个针对Java虚拟机的响应式工具包，它是多语言的(例如，支持多种编程语言)。
在这节课中，我们将重点讨论Java，但也可以用JavaScript、Groovy、Ruby、Ceylon、Scala和Kotlin构建相同的应用程序。

Eclipse Vert.x是事件驱动和非阻塞的，这意味着在Vert.x可以使用少量内核线程处理大量并发请求。
Vert.x允许你的应用程序在最少的硬件下伸缩。

Vert.x具有令人难以置信的灵活性——无论是它的网络实用程序、复杂的现代web应用程序、HTTP/REST微服务、高容量事件处理还是成熟的后端消息总线应用程序Vert.x非常适合。

Vert.x被许多 [不同的公司](http://vertx.io/whos_using/) 使用，从实时游戏到银行等等。

Vert.x不是一个限制框架或容器，我们也不会告诉你如何正确地编写应用程序。相反，我们给你很多有用的砖块，让你以你想要的方式创建你的应用程序。

Vert.x很有趣——再次享受成为开发者的乐趣吧。与受限的传统应用程序容器不同，Vert.x为您提供了令人难以置信的能力和敏捷性，以您想要的方式，以您想要的语言创建引人注目的、可伸缩的21世纪应用程序，而且不需要太多麻烦。

* Vert.x是轻量级-Vert.x内核的大小约为650kB。
* Vert.x是快。这里有一些独立的[数字](https://www.techempower.com/benchmarks/#section=data-r8&amp;hw=i7&amp;test=plaintext)。
* Vert.x不是应用服务器。没有单一的Vert.x实例，您可以将应用程序部署到其中。你可以在任何你想要的地方运行你的应用。
* Vert.x是模块化的——当你需要更多的bits时，只需要添加你需要的bits就可以了。
* Vert.x简单但不过分简单化。Vert.x允许你简单地创建强大的应用程序。
* Vert.x是创建轻量级、高性能微服务的理想选择。