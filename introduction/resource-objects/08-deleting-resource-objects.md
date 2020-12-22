如果需要删除整个应用程序或单个资源，可以使用 ``oc delete`` 命令。可以通过名称删除特定的资源对象，或者通过使用标签匹配资源对象的子集来删除它们。

要按名称删除单个资源对象，请提供名称:

 ``oc delete route/parksmap-fqdn``{{execute}}

若要使用标签删除特定类型的所有资源对象，请提供资源对象类型名称和选择器。

 ``oc delete route --selector app=parksmap``{{execute}}

在使用标签选择器时，可以通过用逗号分隔资源对象类型名来列出多个资源对象类型名。

 ``oc delete svc,route --selector app=parksmap``{{execute}}

 ``all`` 的捷径还可以用于匹配与应用程序的构建和部署直接相关的所有关键资源对象类型。

 ``oc delete all --selector app=parksmap``{{execute}}

建议在删除任何资源对象之前，使用具有相同参数的 ``oc get`` 来确认要删除的内容。对于 ``oc delete all`` 命令的最后一个变体来说，这一点尤其重要。也就是说，没有提供选择器。

在这种情况下，将删除项目中所有匹配的资源对象。因为存在意外删除所有工作的危险，所以还需要提供 ``--all`` 选项，以确认您确实希望从项目中删除所有资源对象。

 ``oc delete all --all``{{execute}}