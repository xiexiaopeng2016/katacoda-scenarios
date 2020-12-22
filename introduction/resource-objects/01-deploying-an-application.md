在开始本课程之前，您需要部署一个要使用的示例应用程序。

第一步是确保您以 ``developer`` 用户的身份登录。

``oc login --username developer --password developer``{{execute}}

接下来，创建一个新项目来添加应用程序，运行:

``oc new-project myproject``{{execute}}

这将自动切换到新项目，这样您就可以部署应用程序了。

您将要部署的应用程序是在OpenShift开发人员入门Katacoda课程中使用的ParksMap web应用程序。

``oc new-app openshiftroadshow/parksmap-katacoda:1.2.0 --name parksmap``{{execute}}

默认情况下，当从命令行使用 ``oc new-app`` 来部署应用程序时，该应用程序不会公开给公众。因此，作为我们的最后一步，您需要公开服务，以便人们能够访问它。

``oc expose svc/parksmap``{{execute}}

现在可以开始调查已创建的资源对象了。