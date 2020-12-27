现在我们将检查您拉出的URL的不同部分。最常见的命令是这样的，其中只指定存储库的名称:

``podman inspect ubi7/ubi``{{execute}}

但是，到底发生了什么?与DNS类似，podman命令行解析注册服务器上存储库的完整URL和标记。下面的命令会给你同样的结果:

``podman inspect registry.access.redhat.com/ubi7/ubi:latest``{{execute}}

你可以运行以下任何命令，你会得到完全相同的结果，以及:

``podman inspect registry.access.redhat.com/ubi7/ubi:latest``{{execute}}

``podman inspect registry.access.redhat.com/ubi7/ubi``{{execute}}

``podman inspect ubi7/ubi:latest``{{execute}}

``podman inspect ubi7/ubi``{{execute}}

现在，让我们构建另一个图像，但是给它一个标签，而不是“latest”:

``podman build -t ubi7:test -f ~/labs/lab2-step1/Dockerfile``{{execute}}

现在，注意还有另一个标签

``podman images``{{execute}}

现在再试一次解决问题的技巧。发生了什么事?

``podman inspect ubi7``{{execute}}

它失败了，但为什么呢?请使用更完整的URL重试:

``podman inspect ubi7:test``{{execute}}

注意，podman解析容器图像的方式类似于DNS解析。每个容器引擎都是不同的，Docker实际上会解决一些podman不能解决的问题，因为没有关于图像uri如何解析的标准。如果您测试的时间足够长，您将会发现许多关于名称空间、存储库和标记解析的其他注意事项。通常，最好总是使用完整的URI，指定服务器、名称空间、存储库和标记。在构建脚本时请记住这一点。容器看起来似乎很简单，但您需要注意细节。