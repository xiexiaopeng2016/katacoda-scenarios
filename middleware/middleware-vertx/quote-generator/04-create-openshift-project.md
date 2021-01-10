## 红帽OpenShift容器平台

Red Hat OpenShift容器平台是Red Hat OpenShift应用程序运行时(如Vert.x)的首选运行时。OpenShift容器平台基于Kubernetes, Kubernetes可能是在生产环境中运行的容器最常用的编排。OpenShift是目前唯一一个基于Kuberenetes提供多租户的容器平台。这意味着，在提交到共享代码存储库之前，开发人员可以有自己的个人、独立的项目来测试和验证应用程序。

OpenShift还提供了一个功能丰富的web控制台和命令行工具，为用户提供了一个友好的界面，以使用部署到平台上的应用程序。

**1. 登录到OpenShift容器平台**

在第1个终端执行此操作。要登录，我们将使用oc命令，然后像这样指定用户名和密码:

``oc login https://[[HOST_SUBDOMAIN]]-8443-[[KATACODA_HOST]].environments.katacoda.com -u developer -p developer --insecure-skip-tls-verify=true``{{execute interrupt}}

祝贺您，您现在已经通过OpenShift服务器的身份验证。

 **重要的** 是:如果上面的oc登录命令似乎没有做任何事情，您可能已经忘记从上一步停止应用程序。点击终端并按CTRL-C停止应用程序，然后再次尝试上面的oc登录命令!

**2. 创建项目**

项目是帮助您组织部署的顶级概念。OpenShift项目允许一个用户社区(或一个用户)独立于其他社区组织和管理其内容。每个项目都有自己的资源、政策(谁能或不能执行操作)和约束(资源的配额和限制，等等)。项目充当您(或您的团队)在工作中使用的所有应用程序服务和端点的包装器。

对于这个场景，让我们创建一个用于存放应用程序的项目。

``oc new-project vertx-kubernetes-workshop``{{execute}}

``oc policy add-role-to-group edit system:serviceaccounts -n vertx-kubernetes-workshop``{{execute}}

第一条指令创建项目。第二条指令授予权限，以便使用OpenShift的所有功能。

**3.打开OpenShift Web控制台**

OpenShift附带了一个基于web的控制台，允许用户通过浏览器执行各种任务。要了解web控制台是如何工作的，请单击"本地网络浏览器"选项卡旁边的"OpenShift控制台"选项卡。

![OpenShift Console Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/openshift-console-tab.png)

使用以下凭据登录:

* 用户名:``developer``
* 密码:``developer``

您应该看到新创建的项目。点击它。它是空的，所以让我们部署我们的第一个应用程序。