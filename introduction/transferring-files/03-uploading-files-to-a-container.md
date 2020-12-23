要将文件从本地机器复制到容器，将再次使用 ``oc rsync`` 命令。

从本地机器复制文件到容器时，命令的形式是:

```
oc rsync ./local/dir <pod-name>:/remote/dir
```

与从容器复制到本地机器不同，这里没有用于复制单个文件的表单。要只复制选定的文件，您将需要使用 ``--exclude`` 和 ``--include`` 选项来过滤从指定目录复制的文件和未复制的文件。

为了演示复制单个文件的过程，考虑这样一种情况:您部署了一个网站，但没有包含 ``robots.txt`` 文件，但需要快速阻止正在爬行的web机器人。

获取网站当前 ``robots.txt`` 文件的请求失败，HTTP  ``404 Not Found`` 响应。

``curl --head http://blog-myproject.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/robots.txt``{{execute}}

创建一个要上传的 ``robots.txt`` 文件。

``cat > robots.txt << !
User-agent: *
Disallow: /
!``{{execute}}

对于正在使用的web应用程序，它在应用程序源代码的 ``htdocs`` 子目录中托管静态文件。上传 ``robots.txt`` 文件运行:

``oc rsync . $POD:/opt/app-root/src/htdocs --exclude=* --include=robots.txt --no-perms``{{execute}}

如前所述，复制单个文件是不可能的，因此我们指出应该复制当前目录，但是使用 ``--exclude=*`` 选项首先说明在执行复制时应该忽略所有文件。然后使用 ``--include=robots.txt`` 文件覆盖 ``robots.txt`` 文件的模式，确保复制 ``robots.txt`` 文件。

当将文件复制到容器时，需要将文件复制到的目录存在，并且该目录对运行容器的用户或组可写。应该将目录和文件的权限设置为构建镜像过程的一部分。

在上面的命令中，还使用了 ``--no-perms`` 选项，因为容器中的目标目录虽然可由运行容器的组写入，但却由不同的用户拥有，而不是运行容器的用户。这意味着尽管可以将文件添加到目录中，但不能更改现有目录的权限。 ``--no-perms`` 选项告诉 ``oc rsync`` 不要尝试更新权限，以避免失败并返回错误。

上传了 ``robots.txt`` 文件后，再次获取 ``robots.txt`` 文件就成功了。

``curl http://blog-myproject.[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/robots.txt``{{execute}}

这在不需要采取任何进一步操作的情况下工作，因为Apache HTTPD服务器用于托管静态文件，它将自动检测目录中存在新文件。

如果要复制一个完整目录而不是复制单个文件，请去掉 ``--include`` 和 ``--exclude`` 选项。要将当前目录的全部内容复制到容器中的 ``htdocs`` 目录，运行:

``oc rsync . $POD:/opt/app-root/src/htdocs --no-perms``{{execute}}

只是要注意，这将是一切，包括名义上隐藏的文件或目录以“。”开头。因此，您应该非常小心，如果必要的话，可以更具体地使用 ``--include`` 或 ``--exclude`` 选项来限制复制的文件或目录集。