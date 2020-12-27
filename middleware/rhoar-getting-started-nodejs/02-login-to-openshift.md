Red Hat OpenShift容器平台是 **Red Hat OpenShift应用程序运行时** 的首选运行时
像 **node.js** 。OpenShift容器平台基于 **Kubernetes** , Kubernetes是生产环境中最常用的容器编排。 **OpenShift** 是目前基于Kubernetes的唯一一个提供多租户的容器平台。这意味着开发人员可以有他们自己独立的项目来测试
在将应用程序提交到共享代码存储库之前验证它们。

OpenShift还附带了功能丰富的web控制台和命令行工具，为用户提供了一个很好的
接口，以使用部署到平台上的应用程序。

 **1. 登录到OpenShift容器平台**

为了登录，我们将使用 **oc** 命令，然后指定我们的服务器
想要认证到:

``oc login [[HOST_SUBDOMAIN]]-8443-[[KATACODA_HOST]].environments.katacoda.com --insecure-skip-tls-verify=true``{{execute}}

输入您的用户名和密码:

* 用户名: **developer**
* 密码: **developer**

祝贺您，您现在已经通过OpenShift服务器的身份验证。

> 如果上面的 ``oc login`` 命令似乎没有做任何事情，那么您可能忘记从前面的命令停止应用程序了的一步。点击终端并按CTRL-C停止应用程序，然后重试 ``oc login`` !

 **2. 创建项目**

 [项目](https://docs.openshift.com/container-platform/3.6/architecture/core_concepts/projects_and_users.html#projects) 是帮助您组织部署的顶级概念。一个OpenShift项目允许一个用户群体(或一个用户)来组织和管理其内容与其他群体隔离。每个项目都有自己的项目资源、策略(谁能或不能执行操作)和约束(配额, 资源限制等)。项目就像一个包装器, 围绕着您(或您的团队)在工作中使用的应用程序服务和端点。

对于这个场景，让我们创建一个用于存放应用程序的项目。

``oc new-project example --display-name="Sample Node.js External Config App"``{{execute}}

 **3. 打开OpenShift Web控制台**

OpenShift附带一个基于web的控制台，允许用户通过浏览器执行各种任务。要感受一下web控制台
如何工作，点击"本地网络浏览器"选项卡旁边的"OpenShift控制台"选项卡。

![OpenShift Console Tab](/openshift/assets/middleware/rhoar-getting-started-nodejs/openshift-console-tab.png)

您将看到的第一个屏幕是身份验证屏幕。输入您的用户名和密码，然后登录:

![Web Console Login](/openshift/assets/middleware/rhoar-getting-started-nodejs/login.png)

在对web控制台进行身份验证之后，您将看到一个用户有权使用的项目列表。

![Web Console Projects](/openshift/assets/middleware/rhoar-getting-started-nodejs/projects.png)

单击您的新项目名称，将带到项目概述页面它会列出你们所有作为项目的一部分正在运行的路由、服务、部署和pod:

![Web Console Overview](/openshift/assets/middleware/rhoar-getting-started-nodejs/overview.png)

现在那里什么都没有，但即将改变。