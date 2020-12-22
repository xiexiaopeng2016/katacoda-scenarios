该场景由两个OpenShift集群组成:

*  ``cluster1`` 充当主机集群(Terminal Host 1选项卡)

*  ``cluster2`` 作为成员集群(Terminal Host 2选项卡)

你可以访问两个终端，但是大部分工作将在 ``cluster1`` 终端上完成。

为了方便您，已经在每个集群中创建了具有 ``cluster-admin`` 特权的 ``admin`` 用户。

 _注意:_ 当前KubeFed控制平面部署需要集群管理权限。这个需求可以在接下来的版本中解决，因此KubeFed控制飞机的特定角色将可用。

您应该已经以admin的身份登录。为了验证它:

 **集群1** 

``oc whoami``{{execute HOST1}}

 **集群2** 

``oc whoami``{{execute HOST2}}

下一步是克隆托管本课程中使用的代码的Git存储库。从 ``cluster1``  _终端_ ，运行以下命令:

``git clone https://github.com/openshift/federation-dev.git``{{execute HOST1}}

一旦克隆了存储库，将目录更改为新的目录:

``cd federation-dev``{{execute HOST1}}

签出Katacoda分支:

``git checkout katacoda``{{execute HOST1}}

您可能需要检查环境中已经存在的一些配置:

* 上下文创建:您应该会看到配置中已经出现了cluster1和cluster2上下文，这些上下文将在课程中使用。

 **集群1** 

``oc config get-contexts``{{execute HOST1}}

 **集群2** 

``oc config get-contexts``{{execute HOST2}}


* Kubefedctl工具已下载:您应该会看到Kubefedctl工具的版本输出。

 **集群1** 

``kubefedctl version``{{execute HOST1}}

 **集群2** 

``kubefedctl version``{{execute HOST2}}
