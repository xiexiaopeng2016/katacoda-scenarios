部署JupyterHub需要比部署JupyterHub镜像做更多的工作，因此可以使用模板来简化这一任务。

与jupiter notebook和JupyterHub图像一样，本研讨会已经为您加载了这些图像。

要验证模板是否已经为你加载，运行:

``oc get templates``{{execute}}

已经加载的OpenShift模板的目的是:

* `jupyterhub-deployer` -使用现有的jupyter笔记本图像部署JupyterHub服务的模板。
* `jupyterhub-builder` -使用源到镜像(S2I)针对托管的Git存储库构建自定义JupyterHub镜像的模板。自定义的JupyterHub配置将与基础的JupyterHub图像相结合。
* `jupyterhub-quickstart` -部署JupyterHub服务的模板，使用使用源到图像(S2I)构建的自定义Jupyter笔记本图像。
* `jupyterhub-workspace` -部署JupyterHub服务的模板，带有可选的jupiter笔记本的持久存储，并带有使用OpenShift集群身份验证的访问门控。实例还可以访问集群，以部署笔记本所需的额外工作负载。

在这个研讨会中，您将使用``jupyterhub-workspace``模板。
