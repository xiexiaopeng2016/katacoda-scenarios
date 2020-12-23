在本课程中，您学习了如何使用新的服务目录和内置在OpenShift 3.7模板服务代理，您可以轻松部署数据库，然后将其绑定到应用程序。

提供的服务的任何细节都存储在一个 _秘密_ 中，可以使用环境变量或通过卷挂载注入到应用程序中。然后，应用程序代码只需要检查这些，并在连接到服务时使用它们，例如在本课程中使用的数据库。

有关服务目录和模板服务代理的详细信息，请参阅:

* [https://docs.openshift.org/latest/architecture/service_catalog/index.html](https://docs.openshift.org/latest/architecture/service_catalog/index.html)
* [https://docs.openshift.org/latest/architecture/service_catalog/template_service_broker.html](https://docs.openshift.org/latest/architecture/service_catalog/template_service_broker.html)