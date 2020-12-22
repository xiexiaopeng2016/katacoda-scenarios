访问OpenShift并与之交互的最简单方法是通过web控制台。web控制台的URL将由OpenShift集群在设置时指定的公开URL指定。一旦访问了web控制台，您随后的登录方式将取决于配置的标识提供者。

在本课程中，web控制台的公共URL为:

``https://console-openshift-console-[[HOST_SUBDOMAIN]]-443-[[KATACODA_HOST]].environments.katacoda.com``{{copy}}

要在查看这些指令的同时查看web控制台，您还可以在嵌入的 _Terminal_ 选项卡右边选择 _Console_ 选项卡。

在OpenShift集群使用用户身份验证管理的情况下，web控制台登录页面将提示你输入 _Username_ 和 _Password_ 。

![Web Console Login](../../assets/introduction/cluster-access-44/01-web-console-login.png)

在使用一个外部身份验证服务作为身份提供者的情况下，首先需要登录到外部服务。例如, 如果你正在访问 [OpenShift Online](https://www.openshift.com/get-started/) 您会看到:

![External Login](../../assets/introduction/cluster-access-44/01-external-identity-provider.png)

对于本课程中使用的OpenShift集群，由于OpenShift集群正在使用用户身份验证管理，您将看到一个登录页面，提示您输入用户帐户凭据。您可以使用以下凭证登录:

* **Username:** ``developer``{{copy}}
* **Password:** ``developer``{{copy}}

因为这是您第一次以这个用户的身份登录到这个OpenShift集群中，您将看到一条“欢迎来到OpenShift”消息，并可以选择创建一个新项目。

![Web Console Welcome](../../assets/introduction/cluster-access-44/01-web-console-welcome.png)

通过选择  _Create Project_ 创建一个新项目。把项目命名为 ``myproject``{{copy}} 。

![Create New Project](../../assets/introduction/cluster-access-44/01-create-new-project.png)

在创建一个项目之后，您将留在新项目的概览页面上。

如果您想要获得所有可用项目的列表，您可以从左侧菜单中选择 "Home->Projects" 。如果您没有看到菜单，您可以单击web控制台顶层角上的汉堡包菜单项按钮。

![List of Projects](../../assets/introduction/cluster-access-44/01-list-of-projects.png)
