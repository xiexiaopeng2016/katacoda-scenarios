# 添加健康检查

我们当前应用程序的一个限制是，我们没有为OpenShift提供正确监视它的方法。最理想的情况是，我们应该添加一个特定的健康检查路径，所以请检查 [健康检查任务](https://access.redhat.com/documentation/en-us/red_hat_openshift_application_runtimes/1/html/eclipse_vert.x_runtime_guide/missions-intro#mission-health-check-vertx) ，但目前我们将添加一个对'/'的简单调用，以检查Vert.x实例是活的并且正在响应。

## 健康检查的警告

打开 [OpenShift webconsole部署配置页面](https://[[HOST_SUBDOMAIN]]-8443-[[KATACODA_HOST]].environments.katacoda.com/console/project/dev/browse/dc/http-vertx?tab=configuration) 

然后您将看到以下警告

![Health Check Warning](/openshift/assets/middleware/rhoar-getting-started-vertx/health-check-warning.png)

这只是一个警告，您的容器可能100%正确地工作，但如果没有配置适当的健康检查，OpenShift就无法判断应用程序是否正确地响应。

# 监视应用程序是否正确响应

**1. 添加健康检查**

打开``pom.xml``{{Open}}文件，在 ``<!-- ADD HEALTH CHECK HERE -->`` 注释处添加以下行。

<pre class="file" data-filename="pom.xml" data-target="insert" data-marker="<!-- ADD HEALTH CHECK HERE -->">
  <config>
    <vertx-health-check>
      <path>/</path>
    </vertx-health-check>
  </config>
</pre>

在做了这个更改之后，fabric8:plugin有足够的细节来为我们创建健康检查，现在我们可以使用激活的健康检查重新部署我们的应用程序

**2. 重新部署应用程序**

再次运行fabric8:deploy目标，重新部署应用程序。

``mvn fabric8:undeploy fabric8:deploy -Popenshift``{{execute}}

等待展示完成。

``oc rollout status dc/http-vertx``{{execute}}

检查 [OpenShift webconsole部署配置页面](https://[[HOST_SUBDOMAIN]]-8443-[[KATACODA_HOST]].environments.katacoda.com/console/project/dev/browse/dc/http-vertx?tab=configuration) 上的警告是否已经消失

**3.测试**

下面是一个相当复杂的命令，它同时执行多个步骤。在命令之后，将更详细地解释不同的步骤。

``oc --server https://$(hostname):8443 --insecure-skip-tls-verify=true rsh $(oc get pods -l app=http-vertx -o name) pkill java && oc get pods -w``{{execute}}

 ``oc get pods -l app=http-vertx -o name`` 将返回运行pod的名称，每次都是不同的。

 ``oc rsh <pod> pkill java`` 停止应用程序。

 ``oc get pods -w`` 将在一段时间内监视豆荚，并向豆荚报告任何状态变化，例如，如果它们崩溃了，需要重新启动，等等。

在一个新的pod启动并运行后，键入 **CTRL+c** 以停止对pod状态的监视。

现在，验证应用程序已经恢复并再次响应。