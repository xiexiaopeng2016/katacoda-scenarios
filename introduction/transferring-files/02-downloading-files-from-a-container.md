为了演示在运行的容器之间传输文件，我们首先需要部署一个应用程序。运行下面的命令:

``oc new-app openshiftkatacoda/blog-django-py --name blog``{{execute}}

为了能够从web浏览器访问它，我们还需要通过创建一个路由来公开它。

``oc expose svc/blog``{{execute}}

要监视应用程序运行的部署:

``oc rollout status dc/blog``{{execute}}

一旦部署完成并且web应用程序准备就绪，命令将退出。

部署的结果将是运行的容器。你可以看到对应于这个应用程序正在运行的容器的pods的名称，运行:

``oc get pods --selector deploymentconfig=blog``{{execute}}

你只有一个应用程序实例，所以只有一个pod将被列出，类似于:

```
NAME           READY     STATUS    RESTARTS   AGE
blog-1-9j3p3   1/1       Running   0          1m
```

对于需要与pod交互的后续命令，您将需要使用pod的名称作为参数。

为了使在这些指令中引用pod的名称更容易，我们在这里定义了一个外壳函数来捕获该名称，这样它就可以存储在一个环境变量中。然后将在运行的命令中使用该环境变量。

我们将从shell函数中运行命令来获取pod的名称，如下所示:

``oc get pods --selector deploymentconfig=blog -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'``{{execute}}

如上所述，它使用带标签选择器的 ``oc get pods`` ，但我们也使用 ``jsonpath`` 查询来提取运行pod的名称。

要创建shell函数，请运行:

``pod() { local selector=$1; local query='?(@.status.phase=="Running")'; oc get pods --selector $selector -o jsonpath="{.items[$query].metadata.name}"; }``{{execute}}

要在 ``POD`` 环境变量中为这个应用程序捕获pod的名称，运行:

``POD=`pod deploymentconfig=blog`; echo $POD``{{execute}}

要在运行应用程序的同一个容器中创建交互式shell，可以使用 ``oc rsh`` 命令，为它提供保存pod名称的环境变量。

``oc rsh $POD``{{execute}}

在交互式shell中，查看应用程序目录中存在哪些文件。

``ls -las``{{execute}}

这将产生类似于:

```
total 80
 0 drwxrwxr-x. 1 default    root    52 Oct 24 02:51 .
 0 drwxrwxr-x. 1 default    root    28 Jun 18 02:10 ..
 4 -rwxrwxr-x. 1 default    root  1454 Jun 18 02:07 app.sh
 0 drwxrwxr-x. 1 default    root    43 Jun 18 02:11 blog
 0 drwxrwxr-x. 2 default    root    25 Jun 18 02:07 configs
 4 -rw-rw-r--. 1 default    root   230 Jun 18 02:07 cronjobs.py
44 -rw-r--r--. 1 1000520000 root 44032 Oct 24 02:51 db.sqlite3
 4 -rw-rw-r--. 1 default    root   430 Jun 18 02:07 Dockerfile
 0 drwxrwxr-x. 2 default    root    25 Jun 18 02:07 htdocs
 0 drwxrwxr-x. 1 default    root    25 Jun 18 02:11 katacoda
 4 -rwxrwxr-x. 1 default    root   806 Jun 18 02:07 manage.py
 0 drwxrwxr-x. 3 default    root    20 Jun 18 02:11 media
 0 drwxrwxr-x. 1 default    root    19 Apr  3  2019 .pki
 4 -rw-rw-r--. 1 default    root   832 Jun 18 02:07 posts.json
 8 -rw-rw-r--. 1 default    root  7861 Jun 18 02:07 README.md
 4 -rw-rw-r--. 1 default    root   203 Jun 18 02:07 requirements.txt
 4 -rw-rw----. 1 default    root  1024 Apr  3  2019 .rnd
 0 drwxrwxr-x. 4 default    root    57 Jun 18 02:09 .s2i
 0 drwxrwxr-x. 4 default    root    30 Jun 18 02:11 static
 0 drwxrwxr-x. 2 default    root   148 Jun 18 02:07 templates
```

对于正在使用的应用程序，这已经创建了一个数据库文件:

```
44 -rw-r--r--. 1 1000520000 root 44032 Oct 24 02:51 db.sqlite3
```

让我们看看如何将这个数据库文件复制回本地计算机。

要确认文件位于容器内的哪个目录，运行以下命令:

``pwd``{{execute}}

这应该显示:

```
/opt/app-root/src
```

退出交互式shell并返回到本地机器运行:

``exit``{{execute}}

要将文件从容器复制到本地机器，可以使用 ``oc rsync`` 命令。

当从容器复制单个文件到本地机器时，命令的形式是:

```
oc rsync <pod-name>:/remote/dir/filename ./local/dir
```

复制单个数据库文件运行:

``oc rsync $POD:/opt/app-root/src/db.sqlite3 .``{{execute}}

这应该显示输出类似于:

```
receiving incremental file list
db.sqlite3

sent 43 bytes  received 44,129 bytes  88,344.00 bytes/sec
total size is 44,032  speedup is 1.00
```

运行以下命令检查当前目录的内容:

``ls -las``{{execute}}

您应该会看到本地计算机现在有了文件的副本。

```
44 -rw-r--r--  1 root root 44032 Oct 24 04:15 db.sqlite3
```

请注意，要将文件复制到的本地目录必须存在。如果您不想将其复制到当前目录中，请确保目标目录已预先创建。

除了复制单个文件外，还可以复制目录。将目录复制到本地机器的命令形式为:

```
oc rsync <pod-name>:/remote/dir ./local/dir
```

要从容器中复制 ``media`` 目录，运行:

``oc rsync $POD:/opt/app-root/src/media .``{{execute}}

如果要在复制目录时重命名目录，应该首先用想要使用的名称创建目标目录。

``mkdir uploads``{{execute}}

然后复制文件使用命令:

``oc rsync $POD:/opt/app-root/src/media/. uploads``{{execute}}

为了确保只复制容器上目录的内容，而不复制目录本身，远程目录将使用 ``/.`` 作为后缀。

注意，如果目标目录包含与容器中的文件同名的现有文件，则本地文件将被覆盖。如果目标目录中有其他文件，而这些文件不存在于容器中，它们将保持原样。如果您确实想要一个完全相同的副本，其中目标目录总是被更新为与容器中存在的内容完全相同，请使用 ``--delete`` 选项到 ``oc rsync`` 。

在复制目录时，您可以通过使用 ``--exclude`` 和 ``--include`` 选项来指定要针对目录和文件匹配的模式，并根据需要排除或包含它们，从而更有选择性地选择要复制的内容。

如果在一个pod中运行多个容器，则需要使用 ``--container`` 选项指定希望使用哪个容器。