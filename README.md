# 在Katacoda上的OpenShift学习

这是出现在learn.openshift.com上的内容。如果你有任何问题，在这里提出问题。

## 贡献

首先，你要分叉这个回购和注册在 [Katacoda](https://katacoda.com/login) 与你的GitHub handle。

对于每个场景，请执行以下步骤:

1. 处理这个场景，在您自己的环境中进行尝试``https://www.katacoda.com/$GITHUBHANDLE``
2. 当你感到满意时，发送一个拉入请求，提及你在第一步中创建的问题。
3. 接下来，从团队成员那里获得两个评论/好评(如果你在几天内没有看到任何活动，就在你的问题上提到@btannous或@jdob)
4. 一旦你的方案被审查过，我们将合并它，它将出现在learn.openshift.com上

## 交付一个车间?

重要提示:如果您要交付一个研讨会，请确保您在活动开始前至少 **48小时** 通知了Katacoda团队，但最好是提前一整个星期。没有这一点，我们就不能保证每个人都有能力。如果您是Red Hat的员工，需要使用learn.openshift.com场景安排一个研讨会，请联系osevg@redhat.com获取关于如何设置的信息。

## 内容

### 类别

目前有几个顶级类别。每个类别都有一个路径文件来定义页面上的顺序。主页路径文件是顶层文件，它指向每个catgories。您可以在存储库的顶级目录中找到每个类别的相关路径文件。

* 主页的途径:[https://github.com/openshift-labs/learn-katacoda/blob/master/homepage-pathway.json](https://github.com/openshift-labs/learn-katacoda/blob/master/homepage-pathway.json)

使用聚类路径是一个很好的例子，可以用来理解类别路径是如何构造的:

* 使用聚类路径:[https://github.com/openshift-labs/learn-katacoda/blob/master/using-the-cluster-pathway.json](https://github.com/openshift-labs/learn-katacoda/blob/master/using-the-cluster-pathway.json)

 ``pathway_id`` 指出场景内容可以在哪个目录中找到。让我们来看看该文件中的第一个条目:

```
{
        "external_link": "https://learn.openshift.com/introduction/cluster-access/",
        "pathway_id": "introduction",
        "course_id": "cluster-access",
        "title": "Logging in to an OpenShift Cluster"
 }
```

* 内容:[https://github.com/openshift-labs/learn-katacoda/tree/master/introduction/cluster-access](https://github.com/openshift-labs/learn-katacoda/tree/master/introduction/cluster-access)
* 资产:[https://github.com/openshift-labs/learn-katacoda/tree/master/assets/introduction/cluster-access-44](https://github.com/openshift-labs/learn-katacoda/tree/master/assets/introduction/cluster-access-44)

### 创建一个场景

* 在相应的类别目录中为您的方案创建一个目录。如果您不确定使用哪个类别，@btannous和@jdob可以帮助您。
* 遵循每一步的命名约定
* 如果您想在使用说明中使用图像，您必须将它们放入资产中。请创建一个与您的方案名称匹配的目录，以便我们可以将文件与正确的方案相关联。
* 如果需要将资产复制到节点中才能从shell中使用，则必须将它们放置到``assets/``在您的方案中。请注意，要复制的文件也必须列在您的``index.json``下``assets``关键。

### 内容管理员

要向公众推广一个场景，请将其添加到路径文件中。每个目录中的场景不需要在路径文件中就可以访问，但是您需要知道访问它们的完整路径。

要将场景添加到仪表盘/主页，请在路径文件中包含如下格式的引用:

```
https://learn.openshift.com/<category-directory-name>/<scenario-directory-name>/
```

例如; <https://learn.openshift.com/middleware/fis-deploy-app/> 

要添加一个新类别，创建一个路径/场景文件夹结构，类似于introduction和middleware。通过编辑 <https://github.com/openshift-evangelists/intro-katacoda/blob/master/homepage-pathway.json> 将分类添加到主页

## 资源

* [Katacoda例子](https://katacoda.com/scenario-examples)
* [状态页](https://openshift.status.katacoda.com/)