您可以使用命令行，而不是从web控制台部署现有的容器镜像。在此之前，先删除我们已经部署的应用程序。

为此，您可以从web控制台访问创建的每个资源类型，并逐个删除它们。删除应用程序的更简单方法是从命令行使用 `oc` 程序。

要查看到目前为止已经在项目中创建的所有资源的列表，你可以运行命令:

`oc get all -o name`{{execute}}

这将显示输出类似于:

```
pod/blog-django-py-1-cbp96
pod/blog-django-py-1-deploy
replicationcontroller/blog-django-py-1
service/blog-django-py
deploymentconfig.apps.openshift.io/blog-django-py
imagestream.image.openshift.io/blog-django-py
route.route.openshift.io/blog-django-py
```

您只创建了一个应用程序，因此您应该知道列出的所有资源都与它相关。当您部署了多个应用程序时，您需要识别那些特定于您希望删除的应用程序的应用程序。通过使用标签选择器将命令应用到资源子集，可以做到这一点。

要确定可能向资源添加了哪些标签，请选择一个并在其上显示详细信息。要查看已创建的路由，你可以运行命令:

`oc describe route/blog-django-py`{{execute}}

这应该显示输出类似于:

```
Name:                   blog-django-py
Namespace:              myproject
Created:                2 minutes ago
Labels:                 app=blog-django-py
                        app.kubernetes.io/component=blog-django-py
                        app.kubernetes.io/instance=blog-django-py
                        app.kubernetes.io/part-of=blog-django-py-app
Annotations:            openshift.io/generated-by=OpenShiftWebConsole
                        openshift.io/host.generated=true
Requested Host:         blog-django-py-myproject.2886795274-80-frugo03.environments.katacoda.com
                          exposed on router default (host apps-crc.testing) 2 minutes ago
Path:                   <none>
TLS Termination:        <none>
Insecure Policy:        <none>
Endpoint Port:          8080-tcp

Service:        blog-django-py
Weight:         100 (100%)
Endpoints:      10.128.0.205:8080
```

在本例中，当通过OpenShift web控制台部署现有容器镜像时，OpenShift已自动应用到标签 `app=blog-django-py` 的所有资源。你可以通过运行命令来确认这一点:

`oc get all --selector app=blog-django-py -o name`{{execute}}

这应该显示与运行`oc get all -o name`时相同的资源列表。为了再次检查这是什么正在被描述，运行改为:

`oc get all --selector app=blog -o name`{{execute}}

在本例中，因为没有标签为`app=blog`的资源，结果将为空。

有了选择一个应用程序的资源的方法，你现在可以通过运行命令来调度删除它们:

`oc delete all --selector app=blog-django-py`{{execute}}

要确认资源已被删除，再次运行命令:

`oc get all -o name`{{execute}}

如果您仍然看到列出的任何资源，请继续运行该命令，直到显示它们都已删除为止。您会发现，资源可能不会立即被删除，因为您只安排了删除它们的计划，而它们被删除的速度将取决于应用程序关闭的速度。

尽管可以使用标签选择器来限定要查询或删除的资源，但一定要注意，您可能并不总是需要使用 `app` 标签。当从模板创建应用程序时，应用的标签及其名称由模板指定。因此，模板可以使用不同的标签约定。在删除任何资源之前，总是使用 `oc describe` 来验证应用了哪些标签，使用 `oc get all --selector` 来验证匹配了哪些资源。