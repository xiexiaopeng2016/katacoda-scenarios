我们已经部署了应用程序的第一个版本，并通过浏览器访问它进行了测试。让我们来看看OpenShift和 ``odo`` 是如何帮助我们在应用运行后更容易迭代。

首先，确保您仍然在 ``frontend`` 目录中:

 ``cd ~/frontend``{{execute}}

现在，我们将告诉 ``odo`` 到 ``watch`` 关于后台文件系统的变化。请注意，在本教程的后台包含 ``&`` 来运行 ``odo watch`` ，但它通常只是作为 ``odo watch`` 运行，可以使用 ``ctrl+c`` 终止。

 ``odo watch &``{{execute}}

让我们为我们的狂野西部游戏改变显示的名称。目前，标题是“狂野西部的开放转变之路!”我们将把它改为“My App The OpenShift Way!”

![Application Title](../../assets/introduction/developing-with-odo-42/app-name.png)

用Unix流编辑器 ``sed`` 执行的搜索和替换一行代码编辑文件 ``index.html`` :

 ``sed -i "s/Wild West/My App/" index.html``{{execute}}

在 ``odo`` 识别更改之前可能会有一点延迟。一旦识别到更改， ``odo`` 将把更改推送到 ``frontend`` 组件，并将其状态打印到终端:

```
File /root/frontend/index.html changed
File changed
Pushing files...
✓ Waiting for component to start [10ms]
✓ Syncing files to the component [16s]
✓ Building component [6s]
```

在web浏览器中刷新应用程序的页面。您将在应用程序的web界面中看到新名称。

注意:如果你不再在浏览器中打开应用程序页面，你可以执行以下命令回调url:

 ``odo url list``{{execute interrupt}}