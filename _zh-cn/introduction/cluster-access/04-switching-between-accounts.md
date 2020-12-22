当使用 ``oc`` 命令行工具时，您一次只能与一个OpenShift集群交互。在同一台计算机上，作为同一本地用户打开单独的shell，同时在不同的OpenShift集群上工作，这是不可能的。这是因为当前登录会话的状态存储在运行 ``oc`` 命令的本地用户的主目录中。

如果您确实需要在多个OpenShift集群上工作，或者甚至在同一个OpenShift集群上作为不同的用户，那么您需要记住在它们之间进行切换。

在本课程中，您最初从命令行使用 ``oc login`` 以 ``developer`` 用户登录。随后您以 ``user1`` 用户的身份登录。

此时，您仍然处于登录状态，并拥有两个用户的活动会话令牌，但当前的操作是作为 ``user1`` 用户。

要切换回 ``developer`` 用户运行:

``oc login --username developer``{{execute}}

因为您已经为 ``developer`` 用户提供了密码，所以不会提示您再次提供密码。在切换用户时，只有在活动会话过期时，才会再次提示您提供密码或提供新的会话令牌。

你可以通过运行以下命令来验证你现在是 ``developer`` 用户:

``oc whoami``{{execute}}

如果你在多个OpenShift集群上工作，要在它们之间切换，你再次使用 ``oc login`` ，但只提供OpenShift集群的URL。例如，如果你有一个OpenShift Online免费启动层的帐户，并被分配到 ``us-east-1`` 集群，你可以运行:

``oc login https://api.starter-us-east-1.openshift.com``

在切换使用哪个OpenShift集群时，如果您没有明确说明要使用哪个用户，那么它将使用您最后一次登录的用户，就像在那个集群中一样。如果需要，您仍然可以提供 ``--username`` 。

切换，不需要提供密码或使用令牌注册是可能的，因为每个令牌的详细信息分别保存在所谓的上下文中。你可以通过运行以下命令来查看当前上下文:

``oc whoami --show-context``{{execute}}

你可以通过运行以下命令得到你曾经登录过的所有OpenShift集群的列表:

``oc config get-clusters``{{execute}}

通过运行以下命令，你可以得到所有已经创建的上下文列表，显示你以哪些用户登录过集群，以及你曾经操作过哪些项目:

``oc config get-contexts``{{execute}}
