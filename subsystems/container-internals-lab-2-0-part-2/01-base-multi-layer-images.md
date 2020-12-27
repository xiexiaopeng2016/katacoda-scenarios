本练习的目标是理解基本镜像和多层映像(存储库)之间的区别。另外，尝试理解图像层和存储库之间的区别。

让我们来看看一些基本图像。我们将使用podman history命令检查这些存储库中的所有层。注意，这些容器图像没有父层。这些是基本的图像，它们是被设计来构建的。首先，让我们看看完整的ubi7基图:

``podman history registry.access.redhat.com/ubi7/ubi:latest``{{execute}}

现在，让我们来看看最小基像，它是红帽通用基像(UBI)集合的一部分。注意，它要小得多:

``podman history registry.access.redhat.com/ubi7/ubi-minimal:latest``{{execute}}

现在，使用我们为你创建的一个简单的Dockerfile，建立一个多层次的图像:

``podman build -t ubi7-change -f ~/labs/lab2-step1/Dockerfile``{{execute}}

您看到新创建的ubi7更改标记了吗?

``podman images``{{execute}}

你能看到构成新图像/存储库/标签的所有图层吗?这个命令甚至显示了每个层中运行的命令的简短摘要。这对于探索图像是如何生成的非常方便。

``podman history ubi7-change``{{execute}}

注意，输出中列出的第一个图像ID(底部)与registry.access.redhat.com/ubi7/ubi图像匹配。请记住，在可信来源(即具有来源或维护保管链)的可信基础镜像上构建非常重要。容器存储库由层组成，但我们通常简单地将它们称为“容器图像”;或容器。当架构系统时，我们必须精确地使用我们的语言，否则我们会给最终用户造成混淆。