[Project Jupyter](https://jupyter.org/) 网站将Jupyter笔记本描述为:

> 一个开放源代码的网络应用程序，允许你创建和共享包含实时代码、方程式、可视化和叙述文本的文档。用途包括:数据清洗和转换，数值模拟，统计建模，数据可视化，机器学习，等等。

jupiter笔记本可以直接部署到Linux、macOS或Windows环境中，或者部署到Docker、Kubernetes和OpenShift等容器环境中。

在本研讨会中，您将学习如何为多个用户提供持久的工作空间，以便使用JupyterHub在jupiter笔记本上工作。访问Jupyter笔记本将使用OpenShift集群身份验证。jupiter notebook实例将附加到OpenShift集群，这样用户就可以与jupiter notebook所需的集群进行交互，并将工作负载部署到该集群。

所示的示例将使用来自[Jupyter on OpenShift](https://github.com/jupyter-on-openshift) 项目的示例jupiter notebook镜像、JupyterHub镜像和模板。[Jupyter on OpenShift](https://github.com/jupyter-on-openshift)项目是一个社区项目，用于演示如何将jupiter notebook和JupyterHub部署到OpenShift。