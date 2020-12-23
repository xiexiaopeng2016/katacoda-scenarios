由于应用程序的两个组件都在集群上运行，我们需要将它们连接起来，以便它们能够进行通信。OpenShift提供了将通信绑定从程序发布到其客户机的机制。这就是所谓的链接。

要连接当前的 ``frontend`` 组件到 ``backend`` ，你可以运行:

 ``odo link backend --component frontend --port 8080``{{execute}}

这将把关于 ``backend`` 的配置信息注入到 ``frontend`` 中，然后重新启动 ``frontend`` 组件。

将显示以下输出，以确认连接信息已添加到 ``frontend`` 组件:

```
✓ Component backend has been successfully linked from the component frontend

The below secret environment variables were added to the 'frontend' component:

· COMPONENT_BACKEND_PORT
· COMPONENT_BACKEND_HOST

You can now access the environment variables from within the component pod, for example:
$COMPONENT_BACKEND_HOST is now available as a variable within component frontend
```

如果您通过单击console选项卡快速返回web **控制台** ，您将看到 ``frontend`` 组件的深蓝色环再次变成了浅蓝色。这意味着 ``frontend`` 的pod正在重新启动，以便它现在将运行有关如何连接到 ``backend`` 组件的信息。当前端组件周围再次出现深蓝色环时，链接完成。

一旦链接完成，您可以再次单击 ``frontend`` 组件圆并选择 **查看日志** 。这一次，不是错误消息，而是以下确认 ``frontend`` 与 ``backend`` 组件正确通信:

```
Listening on 0.0.0.0, port 8080
Frontend available at URL_PREFIX: /
Proxying "/ws/*" to 'backend-app:8080'
```

现在 ``frontend`` 组件已经与 ``backend`` 组件链接，让我们让 ``frontend`` 公开访问。