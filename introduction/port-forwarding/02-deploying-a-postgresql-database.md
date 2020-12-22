要创建一个数据库，然后你可以连接，运行命令:

`oc new-app postgresql-ephemeral --name database --param DATABASE_SERVICE_NAME=database --param POSTGRESQL_DATABASE=sampledb --param POSTGRESQL_USER=username --param POSTGRESQL_PASSWORD=password`{{execute}}

这将启动一个PostgreSQL数据库实例。

虽然数据库通常会与持久卷配对，但在本课程中，我们只想演示如何访问数据库。因此，我们在这里创建的数据库实例只将数据库存储在容器本地的文件系统中。这意味着如果重新启动数据库，任何更改都将丢失。当您部署要与自己的应用程序一起使用的数据库时，您可能希望考虑使用持久卷。

要在数据库部署和准备就绪时监控进度，可以运行以下命令:

`oc rollout status dc/database`{{execute}}

一旦数据库准备好使用，该命令将退出。

在前端web应用程序中使用数据库时，需要配置web应用程序以了解数据库。我们这门课会跳过这个。