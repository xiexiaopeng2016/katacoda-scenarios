我们已经更新了 ``frontend`` 与 ``backend`` 连接，以允许我们的应用程序组件进行通信。现在让我们为我们的应用程序创建一个外部URL，这样我们就可以看到它的实际操作:

 ``odo url create frontend --port 8080``{{execute}}

一旦在 ``frontend`` 组件的配置中创建了URL，您将看到以下输出:

```
✓ URL created for component: frontend

To create URL on the OpenShift cluster, please run `odo push`
```

现在可以推动改变了:

 ``odo push``{{execute}}

 ``odo`` 将打印为应用程序生成的URL。它应该位于 ``odo push`` 输出的中间，类似于下面的输出:

```
Validation
 ✓ Checking component [34ms]

Configuration changes
 ✓ Retrieving component data [27ms]
 ✓ Applying configuration [25ms]

Applying URL changes
 ✓ URL frontend: http://frontend-app-myproject.2886795278-80-frugo03.environments.katacoda.com created

Pushing to component frontend of type local
 ✓ Checking file changes for pushing [832029ns]
 ✓ No file changes detected, skipping build. Use the '-f' flag to force the build.
```

一旦 ``odo push`` 命令完成，请访问浏览器中的URL以查看应用程序。