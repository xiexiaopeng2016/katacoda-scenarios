为了知道数据库正在连接到哪里，运行命令:

`oc get pods --selector name=database`{{execute}}

这将输出运行数据库的pod的详细信息。

```
NAME               READY     STATUS    RESTARTS   AGE
database-1-9xv8n   1/1       Running   0          1m
```

为了使引用pod的名称更容易，通过运行以下命令在一个环境变量中捕获pod的名称:

``POD=`oc get pods --selector name=database -o custom-columns=NAME:.metadata.name --no-headers`; echo $POD``{{execute}}

要在运行数据库的同一个容器中创建交互式shell，可以使用``oc rsh``命令，为它提供pod的名称。

`oc rsh $POD`{{execute}}

您还可以通过web浏览器访问交互式终端会话，方法是从web控制台访问pod细节。

您可以通过运行以下命令看到您在运行数据库的容器中:

``ps x``{{execute}}

这将显示输出类似于:

```
PID TTY      STAT   TIME COMMAND
  1 ?        Ss     0:00 postgres
 60 ?        Ss     0:00 postgres: logger process
 62 ?        Ss     0:00 postgres: checkpointer process
 63 ?        Ss     0:00 postgres: writer process
 64 ?        Ss     0:00 postgres: wal writer process
 65 ?        Ss     0:00 postgres: autovacuum launcher process
 66 ?        Ss     0:00 postgres: stats collector process
 67 ?        Ss     0:00 postgres: bgworker: logical replication launcher
193 pts/0    Ss     0:00 /bin/sh
257 pts/0    R+     0:00 ps x
```

因为您在同一个容器中，所以如果容器中提供数据库客户机，此时您可以为数据库运行数据库客户机。对于PostgreSQL，您可以使用`psql`命令。

`psql sampledb username`{{execute}}

这将提示您通过`psql`运行数据库操作。

```
psql (9.5.4)
Type "help" for help.

sampledb=>
```

您现在可以动态地创建数据库表、添加数据或修改现有数据。

退出`psql`，请输入:

`\q`{{execute}}

退出交互式shell运行:

`exit`{{execute}}

您想要对数据库执行的任何操作都可以通过容器中包含的任何数据库管理工具完成。不过，这将被限制在基于控制台的工具，您将不能使用基于GUI的工具，它运行在您的本地机器上，因为数据库仍然没有暴露在OpenShift集群之外。

如果您需要运行数据库脚本文件来执行数据库上的操作，还需要首先使用`oc rsync`命令将这些文件复制到数据库容器中。