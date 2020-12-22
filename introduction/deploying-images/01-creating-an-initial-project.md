在我们开始之前,您需要登录并在OpenShift中创建一个项目来工作。

从 _终端_ 登录到本课程使用的OpenShift集群,运行:

`oc login -u developer -p developer`{{execute}}

这将使用凭证让你登录:

* **用户名:** `developer`
* **密码:** `developer`

您应该会看到输出:

```
Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>
```

要创建一个名为`myproject`的新项目,可以运行以下命令:

`oc new-project myproject`{{execute}}

您应该看到类似的输出:

```
Now using project "myproject" on server "https://openshift:6443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app django-psql-example

to build a new example application in Python. Or use kubectl to deploy a simple Kubernetes application:

    kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
```

切换到 _控制台_ 并使用与上面相同的凭据登录到OpenShift web控制台。

![Web Console Login](../../assets/introduction/deploying-images-44/01-web-console-login.png)

这应该会让您停留在您可以访问的项目列表中。因为我们只创建了一个项目,所有你应该看到的只是`myproject`。

![List of Projects](../../assets/introduction/deploying-images-44/01-list-of-projects.png)

点击`myproject`,然后你应该在项目的 _概述_ 页。为项目选择开发人员视角,而不是左侧菜单中的 _管理员_ 视角。如果有必要,单击网络控制台左上角的汉堡包菜单图标,以显示左边的菜单。

由于项目当前是空的，应该找不到工作负载，您将看到如何部署应用程序的各种选项。

![Add to Project](../../assets/introduction/deploying-images-44/01-add-to-project.png)