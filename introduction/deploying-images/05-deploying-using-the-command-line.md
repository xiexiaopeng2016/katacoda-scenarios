现在您又有了一个干净的项目，所以让我们部署相同的现有容器镜像，但这一次使用 `oc` 命令行程序。

你之前使用的镜像的名称是:

```
openshiftkatacoda/blog-django-py
```

如果已经提供了要部署的镜像的名称，并希望从命令行验证它是否有效，可以使用 `oc new-app --search` 命令。对于这个镜像运行:

`oc new-app --search openshiftkatacoda/blog-django-py`{{execute}}

这应该显示输出类似于:

```
Docker images (oc new-app --docker-image=<docker-image> [--code=<source>])
-----
openshiftkatacoda/blog-django-py
  Registry: Docker Hub
  Tags:     latest
```

它确认在Docker Hub注册中心上可以找到镜像。

要部署镜像，可以运行以下命令:

`oc new-app openshiftkatacoda/blog-django-py`{{execute}}

这将显示类似于:

```
--> Found container image 927f823 (4 months old) from Docker Hub for "openshiftkatacoda/blog-django-py"

    Python 3.5
    ----------
    Python 3.5 available as container is a base platform for building and running various Python 3.5 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.

    Tags: builder, python, python35, python-35, rh-python35

    * An image stream tag will be created as "blog-django-py:latest" that will track this image
    * This image will be deployed in deployment config "blog-django-py"
    * Port 8080/tcp will be load balanced by service "blog-django-py"
      * Other containers can access this service through the hostname "blog-django-py"

--> Creating resources ...
    imagestream.image.openshift.io "blog-django-py" created
    deploymentconfig.apps.openshift.io "blog-django-py" created
    service "blog-django-py" created
--> Success
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/blog-django-py'
    Run 'oc status' to view your app.
```

OpenShift将基于镜像的名称分配一个默认名称，在本例中为 `blog-django-py` 。通过提供 `--name` 选项和希望用作参数的名称，可以指定要给应用程序的不同名称和创建的资源。

与从web控制台部署现有容器镜像不同，应用程序在默认情况下不会暴露在OpenShift集群之外。要公开创建的应用程序，使其在OpenShift集群之外可用，您可以运行以下命令:

`oc expose service/blog-django-py`{{execute}}

通过在_控制台_上选择切换到OpenShift web控制台，以验证应用程序已经部署。在项目的拓扑视图上为应用程序显示的URL快捷方式图标上选择以访问应用程序。

或者，要查看分配给从命令行创建的路由的主机名，你可以运行以下命令:

`oc get route/blog-django-py`{{execute}}