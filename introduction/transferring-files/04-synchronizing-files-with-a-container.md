除了可以选择手动上传或下载文件之外，还可以设置 ``oc rsync`` 命令，以便在本地计算机和容器之间执行实时的文件同步。

也就是说，将监视您本地计算机的文件系统，以防对文件所做的任何更改。当文件发生更改时，更改后的文件将自动复制到容器中。

如果需要，同样的过程也可以在相反的方向上运行，容器中的更改将自动复制回您的本地计算机。

在应用程序开发期间，将更改从本地计算机自动复制到容器中是非常有用的。

脚本编程语言,例如PHP, Python或Ruby,不需要单独的编译阶段,提供手动重启web服务器不会导致集装箱出口,或者web服务器总是重新加载代码文件已被修改,您可以现场表演与您的应用程序运行在OpenShift代码开发。

要演示这种能力，请为您已经部署的web应用程序克隆Git存储库。

``git clone https://github.com/openshift-katacoda/blog-django-py``{{execute}}

这将创建一个包含应用程序源代码的子目录 ``blog-django-py`` :

```
Cloning into 'blog-django-py'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 412 (delta 0), reused 0 (delta 0), pack-reused 409
Receiving objects: 100% (412/412), 68.49 KiB | 701.00 KiB/s, done.
Resolving deltas: 100% (200/200), done.
```

现在运行以下命令，让 ``oc rsync`` 执行代码的实时同步，将 ``blog-django-py`` 目录中的任何更改复制到容器中。

``oc rsync blog-django-py/. $POD:/opt/app-root/src --no-perms --watch &``{{execute}}

在这种情况下，我们是作为一个后台进程运行的，因为我们只有一个终端窗口可用，你可以运行它作为一个前台进程在一个单独的终端，如果这样做自己。

你可以通过运行以下程序来查看后台进程的详细信息:

``jobs``{{execute}}

当您最初运行这个 ``oc rsync`` 命令时，您将看到它复制了文件，因此本地目录和远程目录是同步的。对本地文件所做的任何更改现在都将自动复制到远程目录。

在进行更改之前，使用URL打开我们在单独的浏览器窗口中部署的web应用程序:

http://blog-myproject。[[HOST_SUBDOMAIN]] -80 [[KATACODA_HOST]] .environments.katacoda.com/

您应该会看到网站标题横幅的颜色是红色的。

![Blog Web Site Red](../../assets/introduction/transferring-files-42/04-blog-web-site-red.png)

让我们通过运行命令来改变横幅颜色:

``echo "BLOG_BANNER_COLOR = 'blue'" >> blog-django-py/blog/context_processors.py``{{execute}}

等待查看已更改的文件是否上传，然后刷新web站点的页面。

不幸的是，您将看到标题横幅仍然是红色的。这是因为对于Python来说，任何代码更改都被正在运行的进程缓存，并且有必要重新启动web服务器应用程序进程。

对于这个部署，将使用WSGI服务器 ``mod_wsgi-express`` 。要触发web服务器应用程序进程的重新启动，请运行:

``oc rsh $POD kill -HUP 1``{{execute}}

该命令的作用是向容器内运行的进程ID 1发送HUP信号，该容器是正在运行的 ``mod_wsgi-express`` 的实例。这将触发应用程序所需的重新启动和重新加载，但web服务器实际上并没有退出。

再次刷新web站点的页面，标题横幅现在应该是蓝色的。

![Blog Web Site Blue](../../assets/introduction/transferring-files-42/04-blog-web-site-blue.png)

注意，标题横幅中显示的pod名称没有改变，这表明pod没有重新启动，只有web服务器应用程序进程被重新启动。

手动强制重新启动web服务器应用程序进程将完成这项工作，但是更好的方法是web服务器能够自动检测代码更改并触发重新启动。

对于 ``mod_wsgi-express`` 以及这个web应用程序是如何配置的，可以通过设置部署的环境变量来启用。要设置这个环境变量运行:

``oc set env dc/blog MOD_WSGI_RELOAD_ON_CHANGES=1``{{execute}}

该命令将更新部署配置，关闭现有pod，并用应用程序的新实例替换它，环境变量现在正传递给应用程序。

通过运行以下程序监控应用程序的重新部署:

``oc rollout status dc/blog``{{execute}}

因为现有的pod已经关闭，所以我们需要再次获取pod的新名称。

``POD=`pod deploymentconfig=blog`; echo $POD``{{execute}}

您可能还注意到，我们在后台运行的同步进程可能已经停止。这是因为它连接的豆荚已经关闭。

你可以通过运行:

``jobs``{{execute}}

如果它仍然显示为正在运行，由于未检测到pod的关闭，运行:

``kill -9 %1``{{execute}}

将其杀死。

确保后台任务已经退出:

``jobs``{{execute}}

现在再次运行 ``oc rsync`` 命令，针对新的荚果。

``oc rsync blog-django-py/. $POD:/opt/app-root/src --no-perms --watch &``{{execute}}

再次刷新web站点的页面，标题横幅应该仍然是蓝色的，但您将注意到显示的荚体名称已经更改。

再次修改代码文件，将颜色设置为绿色。

``echo "BLOG_BANNER_COLOR = 'green'" >> blog-django-py/blog/context_processors.py``{{execute}}

再次刷新web站点页面，如果需要多次刷新，直到标题横幅显示为绿色。更改可能不会立即发生，因为文件同步可能需要花费一些时间，检测代码更改和重新启动web服务器应用程序进程也可能需要一些时间。

![Blog Web Site Green](../../assets/introduction/transferring-files-42/04-blog-web-site-green.png)

通过运行以下命令杀死同步任务:

``kill -9 %1``{{execute}}

尽管可以以这种方式将本地计算机中的文件同步到容器中，但是否可以将其作为启用实时编码的机制将取决于所使用的编程语言和所使用的web应用程序堆栈。当使用 ``mod_wsgi-express`` 时，这对于Python是可能的，但对于用于Python的其他WSGI服务器或其他编程语言可能是不可能的。

请注意，即使是在Python的情况下，这只能用于修改代码文件。如果需要安装额外的Python包，则需要从原始源代码重新构建应用程序。这是因为需要对包进行修改，而Python的 ``requirements.txt`` 文件中给出了这一点，在使用这种机制时，不会触发包的安装。