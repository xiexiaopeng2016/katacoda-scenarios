在我们开始之前，您需要登录并在OpenShift中创建一个项目
在工作。

要从 _终端_ 登录到本课程使用的OpenShift群集，
运行:

``oc login -u developer -p developer``{{execute HOST1}}

这将使用凭证登录您:

* **用户名:** ``developer``
* **密码:** ``developer``

您应该会看到输出:

```
Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>
```

要创建一个名为 ``myproject`` 的新项目，运行以下命令:

``oc new-project myproject``{{execute HOST1}}

你应该看到类似的输出:

```
Now using project "myproject" on server "https://openshift:6443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app django-psql-example

to build a new example application in Python. Or use kubectl to deploy a simple Kubernetes application:

    kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
```

在本课程中，我们不打算使用web _控制台_ ，但是如果您想检查web控制台的任何内容，请切换到控制台，并使用与上面从命令行登录时相同的凭据进行登录。