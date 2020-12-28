## 你会学到什么

在这个场景中，您将了解更多关于Node.js的信息，一个包含在 [Red Hat OpenShift应用程序运行时](https://developers.redhat.com/products/rhoar) 的运行时。

您将采用一个现有的示例Node.js应用程序，并对其进行修改，以解决微服务问题，
了解它的结构，将其部署到OpenShift，并练习Node.js应用程序， microservices，OpenShift/Kubernetes之间的接口。

## node.js是什么?

![Logo](/openshift/assets/middleware/rhoar-getting-started-nodejs/logo.png)

Node.js基于谷歌的 [V8 JavaScript引擎](https://developers.google.com/v8/) ，允许你编写服务器端JavaScript
应用程序。它提供了一个基于事件和非阻塞操作的I/O模型，使您能够编写轻量级和高效的应用程序。Node.js还提供了一个大型的模块生态系统叫 [npm](https://www.npmjs.com/) 。查看 [Node.js运行时指南](https://access.redhat.com/documentation/en-us/red_hat_openshift_application_runtimes/1/html-single/node.js_runtime_guide/) ，进一步阅读Node.js和RHOAR。

Node.js运行时允许你在OpenShift上运行Node.js应用程序和服务，同时提供所有OpenShift平台的优势和便利，如滚动更新，持续交付管道、服务发现和canary部署。OpenShift也使您的应用程序更加容易实现常见的微服务模式，如外部化配置、运行状况检查、电路断路器和故障转移。