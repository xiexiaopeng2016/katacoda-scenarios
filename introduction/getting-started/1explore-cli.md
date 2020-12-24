## 命令行接口(CLI)

使用 _oc_ 命令访问OpenShift CLI。从这里，您可以管理整个OpenShift集群并部署新的应用程序。

CLI通过OpenShift增强了底层Kubernetes编配系统。熟悉Kubernetes的用户将能够迅速适应OpenShift。 _oc_ 提供了 _kubectl_ 的所有功能，以及使其更容易使用OpenShift的附加功能。CLI是理想的情况下，您是:

1)直接使用项目源代码

2)编写OpenShift操作脚本

3)受带宽资源限制，无法使用web控制台

在本教程中，我们不关注OpenShift CLI，但我们希望你知道它，以防你更喜欢使用命令行。您可以查看我们的其他课程，更深入地了解CLI的使用。现在，我们将练习登录，这样您就可以获得一些CLI如何工作的经验。

## 练习:使用CLI登录

我们从登录开始吧。您的任务是在控制台输入以下内容:

``oc login``{{execute}}

当出现提示时，输入以下用户名和密码:

 **用户名:** ``developer``{{execute}}

 **密码:** ``developer``{{execute}}

接下来，你可以检查它是否成功:

``oc whoami``{{execute}}

 ``oc whoami`` 应该返回如下响应:

 ``developer`` 

就是这样!

在下一步中，我们将开始使用 **web控制台** 创建您的第一个项目。