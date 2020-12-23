如果您正在为应用程序将一个持久卷挂载到容器中，并且需要将文件复制到容器中，那么可以按照前面描述的方式使用 ``oc rsync`` 来上载文件。您所需要做的就是提供目标目录，即容器中挂载持久卷的路径。

如果您还没有部署应用程序，但是希望预先准备一个持久性卷，其中包含它需要包含的所有数据，那么您仍然可以申请一个持久性卷并将数据上传到它。为了做到这一点，您将需要部署一个虚拟应用程序，持久化卷可以挂载在该应用程序上。

为了创建一个虚拟应用程序，运行以下命令:

``oc run dummy --image centos/httpd-24-centos7``{{execute}}

我们使用 ``oc run`` 命令，因为它只创建一个部署配置和托管pod。没有创建服务，因为我们实际上并不需要在这里运行的应用程序(在本例中是Apache HTTPD服务器的实例)实际上是可接触的。我们使用Apache HTTPD服务器纯粹是作为保持pod运行的一种手段。

要监视pod的启动并确保它已部署，请运行:

``oc rollout status dc/dummy``{{execute}}

一旦它运行，你可以看到创建的资源比使用 ``oc new-app`` 时创建的资源更有限，通过运行:

``oc get all --selector run=dummy -o name``{{execute}}

现在我们有了一个正在运行的应用程序，接下来需要声明一个持久卷，并将它挂载到我们的虚拟应用程序上。在执行此操作时，我们将它分配一个索赔名称为 ``data`` ，以便以后可以通过集合名称引用索赔。我们将持久卷挂载在容器(Linux系统中用于临时挂载卷的传统目录)中的 ``/mnt`` 上。

``oc set volume dc/dummy --add --name=tmp-mount --claim-name=data --type pvc --claim-size=1G --mount-path /mnt``{{execute}}

这将导致我们的虚拟应用程序的新部署，这一次挂载了持久卷。再次监视部署的进度，这样我们就知道什么时候部署完成了，通过运行:

``oc rollout status dc/dummy``{{execute}}

要确认持久卷声明成功，可以运行:

``oc get pvc``{{execute}}

随着虚拟应用程序的运行，以及持久卷的挂载，为运行中的应用程序捕获pod的名称。

``POD=`pod run=dummy`; echo $POD``{{execute}}

我们现在可以使用挂载持久卷的 ``/mnt`` 目录将任何文件复制到持久卷中，作为目标目录。在这种情况下，因为我们正在做一个一次性复制，我们可以使用 ``tar`` 策略代替 ``rsync`` 策略。

``oc rsync ./ $POD:/mnt --strategy=tar``{{execute}}

完成后，您可以通过列出容器内目标目录的内容来验证文件是否传输。

``oc rsh $POD ls -las /mnt``{{execute}}

如果您已经用完了这个持久卷，并且可能需要对另一个持久卷和不同的数据重复这个过程，那么您可以卸载这个持久卷，但保留虚拟应用程序。

``oc set volume dc/dummy --remove --name=tmp-mount``{{execute}}

再次监视该过程，以确认重新部署已经完成。

``oc rollout status dc/dummy``{{execute}}

再次捕获当前荚果的名称:

``POD=`pod run=dummy`; echo $POD``{{execute}}

再看一下目标目录中的内容。此时它应该是空的。这是因为不再挂载持久卷，而您正在查看本地容器文件系统中的目录。

``oc rsh $POD ls -las /mnt``{{execute}}

如果您已经有一个现有的持久卷声明，就像我们现在做的那样，您可以将现有声明的卷挂载到虚拟应用程序中。这与上面同时声明一个新的持久卷并将其挂载到应用程序的方法不同。

``oc set volume dc/dummy --add --name=tmp-mount --claim-name=data --mount-path /mnt``{{execute}}

期待重新部署的完成:

``oc rollout status dc/dummy``{{execute}}

捕捉荚体的名称:

``POD=`pod run=dummy`; echo $POD``{{execute}}

并检查目标目录的内容。我们复制到持久卷的文件应该再次可见。

``oc rsh $POD ls -las /mnt``{{execute}}

完成后，您希望删除虚拟应用程序，使用 ``oc delete`` 来删除它，使用 ``run=dummy`` 的标签选择器来确保我们只删除与虚拟应用程序相关的资源对象。

``oc delete all --selector run=dummy``{{execute}}

检查是否删除了所有资源对象。

``oc get all --selector run=dummy -o name``{{execute}}

虽然我们已经删除了虚拟应用程序，但是持久卷声明仍然存在，以后可以挂载到数据所属的实际应用程序上。

``oc get pvc``{{execute}}