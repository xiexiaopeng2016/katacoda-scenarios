在这个练习中，我们将看一下容器镜像中的内容。Java特别有趣，因为它使用glibc，尽管大多数人没有意识到它。为了证明这一点，我们将使用ldd命令，它显示了二进制文件所链接的所有库。当一个二进制文件被动态链接(库在二进制文件启动时加载)时，必须在系统上安装这些库，否则二进制文件将无法运行。特别是在这个示例中，您可以看到，要让JVM以完全相同的行为运行，就需要以相同的方式编译和链接。换句话说，所有的Java图像都不是一样的:

``podman run -it registry.access.redhat.com/jboss-eap-7/eap70-openshift ldd -v -r /usr/lib/jvm/java-1.8.0-openjdk/jre/bin/java``{{execute}}

注意动态脚本语言也会根据系统库进行编译和链接:

``podman run -it registry.access.redhat.com/ubi7/ubi ldd /usr/bin/python``{{execute}}

检查一个常见的工具，如“卷发”;演示操作系统中使用了多少库。首先，启动RHEL Tools容器。这是Red Hat发布的一个特殊图像，包含了在容器化环境中进行故障排除所需的所有工具。它很大，但也很方便:

``podman run -it registry.access.redhat.com/rhel7/rhel-tools bash``{{execute}}

看看curl所链接的所有库:

``ldd /usr/bin/curl``{{execute}}

让我们来看看哪些包可以提供这些库?OpenSSL和网络安全服务库。当在OpenSSL或NSS中发现一个新的CVE时，需要构建一个新的容器镜像来修补它:

``rpm -qf /lib64/libssl.so.10``{{execute}}

``rpm -qf /lib64/libssl3.so``{{execute}}

退出rhel-tools容器:

``exit``{{execute}}

Apache和其他大多数守护进程和实用程序的情况也类似，它们依赖于库来提供安全性，或者进行深层次的硬件集成:

``podman run -it registry.access.redhat.com/rhscl/httpd-24-rhel7 bash``{{execute}}

Inspect mod_ssl Apache模块:

``ldd /opt/rh/httpd24/root/usr/lib64/httpd/modules/mod_ssl.so``{{execute}}

我们再次找到OpenSSL提供的库:

``rpm -qf /lib64/libcrypto.so.10``{{execute}}

退出httpd24容器:

``exit``{{execute}}

这一切意味着什么?好吧，这意味着你需要准备好重建所有的容器镜像，只要其中一个库存在安全漏洞……