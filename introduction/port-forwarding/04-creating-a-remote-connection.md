为了从运行在您自己的本地机器上的数据库管理工具访问数据库，需要在OpenShift集群之外公开数据库服务。

当web应用程序在OpenShift集群外可见时，就创建了一个路由。这使用户可以使用URL从web浏览器访问web应用程序。路由通常只用于使用HTTP协议的web应用程序。路由不能用于公开数据库，因为它们通常使用自己独特的协议，路由不能与数据库协议一起工作。

有一些方法可以将数据库服务永久地暴露在OpenShift集群之外，但是这样做的需求是例外，而不是常态。如果只是想访问数据库以对其执行管理，您可以使用端口转发创建一个临时连接回您的本地计算机。设置端口转发的行为将在您的本地机器上创建一个端口，然后您可以使用数据库管理工具来连接数据库。

要在本地计算机和运行在OpenShift上的数据库之间设置端口转发，您可以使用`oc port-forward`命令。您需要传递pod的名称和数据库服务正在使用的端口的详细信息，以及要使用的本地端口。

该命令的格式为:

```
oc port-forward <pod-name> <local-port>:<remote-port>
```

要创建一个到PostgreSQL数据库的连接，它使用端口5432，并将它暴露在运行`oc`的本地机器上，作为端口15432，使用:

`oc port-forward $POD 15432:5432 &`{{execute}}

端口15432用于本地机器，而不是5432，以防PostgreSQL实例也在本地机器上运行。如果PostgreSQL实例在本地机器上运行，并且使用了相同的端口，那么连接的设置将会失败，因为该端口已经被使用了。

如果你不知道什么端口可能是可用的，你可以代替使用以下格式的命令:

```
oc port-forward <pod-name> :<remote-port>
```

在这种形式中，关闭本地端口，导致使用随机可用端口。您需要查看命令的输出，以确定本地端口使用了什么端口号并使用它。

当`oc port-forward`命令运行并建立连接时，它将一直运行，直到该命令被中断。然后您将使用一个单独的终端窗口来运行管理工具，该工具可以通过转发的连接进行连接。在本例中，由于我们只有一个终端窗口，所以我们将`oc port-forward`命令作为后台作业运行。

你可以看到它仍然运行使用:

`jobs`{{execute}}

端口转发就绪后，现在可以再次运行`psql`了。这一次它从本地机器运行，而不是在容器内运行。因为转发的连接在本地机器上使用端口15432，所以需要显式地告诉它使用该端口而不是默认的数据库端口。

`psql sampledb username --host=127.0.0.1 --port=15432`{{execute}}

这将再次提示您通过`psql`运行数据库操作。

```
Handling connection for 5432
psql (9.2.18, server 9.5.4)
WARNING: psql version 9.2, server version 9.5.
         Some psql features might not work.
Type "help" for help.

sampledb=>
```

您现在可以动态地创建数据库表、添加数据或修改现有数据。

退出`psql`，输入:

`\q`{{execute}}

因为我们将`oc port-forward`命令作为后台进程运行，所以我们可以使用以下命令终止它:

`kill %1`{{execute}}

再次运行`jobs`，我们可以看到它被终止。

`jobs`{{execute}}

在本练习中，我们使用了`psql`，但是您也可以使用运行在本地机器上的基于GUI的数据库管理工具。