OpenShift项目里的Jupyter提供了Jupyter笔记本和juyterhub镜像，这是专门为了能在OpenShift上最好的工作而构建的。

在部署JupyterHub之前，首先需要将jupiter notebook应用程序和JupyterHub的镜像加载到OpenShift中的项目中。你只需要在一个项目中加载一次。然后，您可以根据需要使用它来创建各种不同的JupyterHub部署。

在这个研讨会中，加载Jupyter笔记本和Jupyterhub镜像的步骤已经为你完成了。

要验证镜像是否已经加载，运行以下命令:

``oc get imagestreams -o name``{{execute}}

您应该看到``s2i-minimal-notebook``和``jupyterhub``镜像流存在。

你可以通过运行以下命令来检查镜像流:

``oc describe imagestream s2i-minimal-notebook``{{execute}}

您应该看到镜像流包含``3.5``和``3.6``的标记。这些对应于Python 3.5和Python 3.6的镜像版本。

在部署JupyterHub时，可以使用这两种用于Jupyter笔记本的镜像，也可以使用您构建的自定义Jupyter笔记本镜像。