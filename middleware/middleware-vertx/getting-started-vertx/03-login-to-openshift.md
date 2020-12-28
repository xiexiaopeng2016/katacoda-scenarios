Red Hat OpenShift容器平台是 **Red Hat OpenShift应用程序运行时** (如 **Vert.x** )的首选运行时。OpenShift容器平台基于 **Kubernetes** , Kubernetes可能是在生产环境中运行的容器最常用的编排。 **OpenShift** 是目前唯一一个基于Kuberenetes提供多租户的容器平台。这意味着，在提交到共享代码存储库之前，开发人员可以有自己的个人、独立的项目来测试和验证应用程序。

OpenShift还提供了一个功能丰富的web控制台和命令行工具，为用户提供了一个友好的界面，以使用部署到平台上的应用程序。

**1. 登录到OpenShift集装箱平台**

要登录，我们将使用 ``oc`` 命令，然后像这样指定用户名和密码:

``oc login [[HOST_SUBDOMAIN]]-8443-[[KATACODA_HOST]].environments.katacoda.com -u developer -p developer --insecure-skip-tls-verify=true``{{execute}}

祝贺您，您现在已经通过OpenShift服务器的身份验证。

> 重要提示:如果上面的 ``oc login`` 命令似乎没有做任何事情，那么您可能忘记从上一个命令停止应用程序了
的一步。点击终端并按 **CTRL-C** 停止应用程序，然后再次尝试上面的 ``oc login`` 命令!

**2. 创建项目**

 [项目](https://docs.openshift.com/container-platform/3.6/architecture/core_concepts/projects_and_users.html#projects) 是帮助您组织部署的顶级概念。一个OpenShift项目允许一个用户群体(或一个用户)来组织和管理其内容与其他群体隔离。每个项目都有自己的项目资源、策略(谁能或不能执行操作)和约束(配额, 资源限制等)。项目就像一个包装器, 围绕着您(或您的团队)在工作中使用的应用程序服务和端点。

对于这个场景，让我们创建一个用于存放应用程序的项目。

``oc new-project dev --display-name="Dev - Eclipse Vert.x Http App"``{{execute}}

**3.打开OpenShift Web控制台**

OpenShift附带一个基于web的控制台，允许用户通过浏览器执行各种任务。要感受一下web控制台如何工作，点击"本地网络浏览器"选项卡旁边的"OpenShift控制台"选项卡。

![OpenShift Console Tab](/openshift/assets/middleware/rhoar-getting-started-vertx/openshift-console-tab.png)

您将看到的第一个屏幕是身份验证屏幕。输入您的用户名和密码，然后登录:

![Web Console Login](/openshift/assets/middleware/rhoar-getting-started-vertx/login.png)

在对web控制台进行身份验证之后，您将看到用户有权查看的项目列表。

![Web Console Projects](/openshift/assets/middleware/rhoar-getting-started-vertx/projects.png)

点击你的新项目名称，它将被带到项目概览页面，该页面将列出你作为项目的一部分创建的所有路由、服务、部署和pod:

![Web Console Overview](/openshift/assets/middleware/rhoar-getting-started-vertx/overview.png)

现在那里什么都没有，但即将改变。