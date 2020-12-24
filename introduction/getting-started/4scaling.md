让我们将应用扩展到pods的2个实例。您可以通过在 _拓扑结构_ 视图中单击 ``parksmap-katacoda`` 应用程序的圆圈内打开侧板来完成此操作。在侧边面板中，单击详细信息选项卡，然后单击“up"旁边的箭头
侧板上的吊舱。

![Scaling using arrows](../../assets/introduction/getting-started-44/4scaling-arrows.png)

要验证我们更改了副本的数量，请单击侧面板中的 _资源_ 选项卡。你应该会看到如下图所示的豆荚列表:

![List of pods](../../assets/introduction/getting-started-44/4scaling-pods.png)

你可以看到我们现在有两个副本。

总的来说，这就是扩展应用程序是多么简单
 _服务_ )。由于OpenShift，应用程序扩展可以非常迅速地发生
是否只是启动现有镜像的新实例，特别是如果该映像
已经缓存在节点上。

### 应用“自我Healing"

openshift&# 39;的 _部署_ 是不断地监视，以查看所需的数字
的pod实际上在运行。因此，如果实际状态偏离了期望的状态(例如，2个pods在运行)，OpenShift将修复这种情况。

既然我们现在有两个舱在运行，让我们看看如果我们运行会发生什么
“accidentally"杀了一个。

缩放到2个副本后，在 _资源_ 选项卡上查看pods列表的地方，通过单击列表中的其中一个pods的名称打开它。

在页面的右上角，有一个 _行动_ 下拉菜单。点击它并选择删除Pod。

![Delete action](../../assets/introduction/getting-started-44/4scaling-actions.png)

单击“ _删除_ Pod”后，在确认对话框中单击“删除”。您将转到一个列出豆荚的页面，然而，这一次，有三个豆荚。注意，在较小的屏幕上，您可能看不到所有这些列。

![List of pods](../../assets/introduction/getting-started-44/4scaling-terminating.png)

我们删除的pod正在终止(即，它正在被清理)。一个新的豆荚被创造，因为
OpenShift将始终确保，如果一个圆荚体死亡，将会有新的圆荚体被创建
填补它的位置。

### 练习:按比例减少

在继续之前，继续将您的应用程序缩小到单个
实例。单击 _拓扑结构_ 以返回 _拓扑结构_ 视图，然后单击 ``parksmap-katacoda`` ，并在 _概述_ 选项卡上单击向下箭头以缩小到一个实例。