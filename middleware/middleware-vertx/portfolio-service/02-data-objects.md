## 数据对象

``Portfolio`` 对象是一个数据对象。事件总线代理支持有限的一组类型，对于不支持的类型，它必须使用数据对象(请查看文档中支持的类型的完整列表)。数据对象是遵循一组约束的Java类:

* 必须用 ``DataObject`` 标注

* 它必须有一个空构造函数、一个复制构造函数和一个以 ``JsonObject`` 为参数的构造函数

* 它必须有一个 ``toJson`` 方法来构建一个表示当前对象的 ``JsonObject``

* 字段必须是属性(getter和setter)

让我们打开 ``io.vertx.workshop.portfolio.Portfolio.java`` 类，看看它是什么样子的:

``portfolio-service/src/main/java/io/vertx/workshop/portfolio/Portfolio.java``{{open}}

如您所见，所有的JSON处理都是由自动生成的 ``converters`` 管理的，因此数据对象非常接近于一个简单的bean。
