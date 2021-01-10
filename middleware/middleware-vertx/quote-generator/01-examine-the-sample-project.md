示例项目显示了基本Vert.x项目的组成部分。根据Maven最佳实践在不同的子目录中布局。

**检查报价生成器项目结构.**

切换到 ``quote-generator`` 项目

``cd /root/code/quote-generator``{{execute}}

让我们来看看这个项目，因为其他每个项目都是用同样的方式构建的。

``tree``{{execute}}

```markdown
.
|-- README.md 
|-- pom.xml 
|-- src
|   |-- kubernetes/config.json
|   |-- main
|   |   |-- fabric8
|   |   |   `-- deployment.yml 
|   |   |-- java
|   |   |   `-- io/vertx/workshop/quote 
|   |   |               |-- GeneratorConfigVerticle.java
|   |   |               |-- MarketDataVerticle.java
|   |   |               `-- RestQuoteAPIVerticle.java
|   |   `-- solution
|   |       `-- io/vertx/workshop/quote 
|   |                   |-- GeneratorConfigVerticle.java
|   |                   |-- MarketDataVerticle.java
|   |                   `-- RestQuoteAPIVerticle.java
|   `-- test
|       |-- java
|       |   `-- io/vertx/workshop/quote 
|       |               |-- GeneratorConfigVerticleTest.java
|       |               `-- MarketDataVerticleTest.java
|       `-- resources 
`-- target
```

>  **注意:** 要生成一个类似的项目框架，你可以访问 [Vert.x Starter](http://start.vertx.io/) 网页。

让我们从 ``pom.xml`` 文件开始。这个文件指定Maven构建:

1. 定义的依赖关系
2. 编译java代码并处理资源(如果有的话)
3. 构建一个fat-jar

fat-jar(也叫 uber jar 或 shaded jar)是一种方便的包装Vert.x应用程序的方法。它会创建一个包含你的应用程序及其所有依赖项的uber-jar，包括Vert.x。然后，要启动它，你只需要使用 ``java -jar <jar name>`` ，而不必处理 ``CLASSPATH`` 。Vert.x并没有规定包装的类型。的确，fat jar很方便，但它们不是唯一的方法。你可以使用普通的(不是fat)jar，OSGi包…
pom.xml文件还包含一组用于配置应用程序的属性:

* ``vertx.verticle``定义主verticle - 入口点
* ``vertx.cluster.name``定义集群的名称