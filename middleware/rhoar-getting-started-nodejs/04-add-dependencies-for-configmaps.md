## 什么是ConfigMap?

ConfigMap是OpenShift用来将配置数据作为简单的键和值对注入到一个或更多的Linux容器中的对象，同时保持容器不受OpenShift的影响。您可以通过多种不同的方式创建ConfigMap对象，包括使用YAML文件，并将其注入到Linux容器中。你可以在 [OpenShift文档](https://docs.openshift.org/latest/dev_guide/configmaps.html) 中找到更多关于ConfigMap的信息。

## 为什么ConfigMap很重要

将应用程序的配置外部化并与代码分离是很重要的。这允许应用程序的配置将随着在不同环境中移动而改变，同时保持代码不变。这也将敏感信息或内部信息排除在代码库和版本控制之外。许多语言和应用程序服务器提供环境变量来支持应用程序配置的外部化。微服务和Linux容器通过添加pods(表示容器的分组)增加了这种复杂性部署和多语言环境。ConfigMaps允许将应用程序配置外部化，并以与语言无关的方式在单个Linux容器和pods中使用。ConfigMaps还允许方便地对配置数据集进行分组和伸缩，这使您能够配置基本的开发、演示和生产之外任意数量的环境。

## 设计权衡

 **优点**

* 配置与部署是分开的
* 可独立更新
* 可以跨服务共享

 **缺点**

* 配置与部署是分开的
* 必须分开维护
* 需要超出服务范围的协调

注意，第一个优点也是第一个缺点。对于云原生应用程序来说，分离配置通常是一个很好的实践，但这是有代价的。然而，正如前面所解释的那样，利远大于弊。让我们修改示例应用程序，使用OpenShift ConfigMaps来分离它的配置!

 **为ConfigMap添加NPM模块**

 [NPM包生态系统](https://www.npmjs.com/) 包含了有助于在Node应用中实现各种功能的项目。为了使我们的示例Node应用程序能够访问OpenShift ConfigMaps，您需要声明一个对新包的依赖。

执行以下命令将新的依赖项插入到 ``package.json`` 文件中:

``npm install "openshift-rest-client@^2.3.0" --save-prod``{{execute}}

这将下载并安装所需的依赖项和更新 ``package.json`` 文件。关闭文件(点击小的'X'附近的文件名)然后重新打开文件(点击这里:``package.json``{{open}})来查看文件底部附近添加的附加依赖项。

使用这个包，应用程序将能够使用ConfigMap从OpenShift访问它的配置。
但是您仍然需要实现访问背后的逻辑，这是您接下来要做的。