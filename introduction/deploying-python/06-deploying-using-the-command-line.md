现在您又有了一个干净的项目，所以让我们部署相同的web应用程序，但是这次使用`oc`命令行工具。

包含web应用程序的Git仓库的URL是:

`https://github.com/openshift-katacoda/blog-django-py`

我们希望使用平台提供的Python最新版本的S2I构建器来部署它。运行下面的命令:

`oc new-app python:latest~https://github.com/openshift-katacoda/blog-django-py`{{execute}}

这应该显示输出类似于:

```
--> Found image 2437334 (6 weeks old) in image stream "openshift/python" under tag "latest" for "python:latest"

    Python 3.6
    ----------
    ...

    Tags: builder, python, python36, python-36, rh-python36

    * A source build using source code from https://github.com/openshift-katacoda/blog-django-py will be created
      * The resulting image will be pushed to image stream tag "blog-django-py:latest"
      * Use 'oc start-build' to trigger a new build
    * This image will be deployed in deployment config "blog-django-py"
    * Port 8080/tcp will be load balanced by service "blog-django-py"
      * Other containers can access this service through the hostname "blog-django-py"

--> Creating resources ...
    imagestream.image.openshift.io "blog-django-py" created
    buildconfig.build.openshift.io "blog-django-py" created
    deploymentconfig.apps.openshift.io "blog-django-py" created
    service "blog-django-py" created
--> Success
    Build scheduled, use 'oc logs -f bc/blog-django-py' to track its progress.
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/blog-django-py'
    Run 'oc status' to view your app.
```

OpenShift会为基于Git存储库名称创建的应用程序分配一个默认名称。在本例中是`blog-django-py`。如果希望更改名称，可以提供`--name`选项以及希望用作参数的名称。

要监视正在运行的构建的日志输出，可以运行以下命令:

`oc logs bc/blog-django-py --follow`{{execute}}

一旦构建完成，此命令将退出。您也可以通过在终端窗口中键入 _CTRL-C_ 来中断该命令。

要查看部署到项目中的任何应用程序的状态，可以运行以下命令:

`oc status`{{execute}}

一旦应用程序的构建和部署完成，你应该看到类似如下的输出:

```
In project myproject on server https://openshift:6443

svc/blog-django-py - 172.30.54.158:8080
  dc/blog-django-py deploys istag/blog-django-py:latest <-
    bc/blog-django-py source builds https://github.com/openshift-katacoda/blog-django-py on openshift/python:latest
    deployment #1 pending 10 seconds ago - 0/1 pods


3 infos identified, use 'oc status --suggest' to see details.
```

与从web控制台部署应用程序的情况不同，应用程序在默认情况下不会暴露在OpenShift集群之外。要公开应用程序，使其在OpenShift集群之外可用，您可以运行以下命令:

`oc expose service/blog-django-py`{{execute}}

通过在_控制台_上选择切换到OpenShift web控制台，以验证应用程序已经部署。

但是您会注意到拓扑视图上的可视化缺少构建和源代码存储库的图标。这是因为在从web控制台创建应用程序时，它们依赖于添加到部署中的特殊注释和标签。当从命令行创建应用程序时，不会自动添加这些注释。如果需要，您可以在以后添加注释。

访问URL的图标仍然显示在可视化视图上。或者，要查看分配给从命令行创建的路由的主机名，你可以运行以下命令:

`oc get route/blog-django-py`{{execute}}