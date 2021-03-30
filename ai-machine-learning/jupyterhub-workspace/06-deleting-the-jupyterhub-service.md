使用完JupyterHub服务后，可以从命令行删除它。

要验证您正在删除正确的资源，首先运行:

``oc get all,configmap,pvc,serviceaccount,rolebinding --selector app=jupyterhub -o name``{{execute}}

这使用一个标签选择器来仅引用此部署的资源。

当你很高兴你将删除正确的资源时，运行:

``oc delete all,configmap,pvc,serviceaccount,rolebinding --selector app=jupyterhub``{{execute}}

这只会从JupyterHub部署到的项目中删除资源。

您还需要删除全局``oauthclient``资源。这是一个单独的步骤，这样您就可以再次检查是否删除了正确的资源。

列出``oauthclient``资源运行:

``oc get oauthclient --selector app=jupyterhub``{{execute}}

按名称删除与此项目中的JupyterHub部署相对应的条目。在这种情况下，项目名称是``myproject``，所以你会运行:

``oc delete oauthclient/jupyterhub-myproject-users``{{execute}}

请注意，这不会删除为用户或由用户创建的任何项目。如果用户没有删除项目本身，作为集群管理员的您将需要识别它们并删除它们。