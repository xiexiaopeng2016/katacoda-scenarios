还可以通过几种不同的方式来修改configmap。在这个步骤，我们将使用OpenShift Web控制台以图形方式(和手动方式)更新ConfigMap。如果需要，这也可以通过编程方式完成。请按照以下步骤:

 **1. 更新ConfigMap内容:**

通过点击选项卡返回OpenShift Web控制台:

![OpenShift Console Tab](/openshift/assets/middleware/rhoar-getting-started-nodejs/openshift-console-tab.png)

如前所述，选择示例应用程序，打开项目的概览页面:

![Overview](/openshift/assets/middleware/rhoar-getting-started-nodejs/overview-populated.png)

从这里，导航到 _资源_ ->ConfigMaps显示 _配置映射_ 列表:

![ConfigMaps](/openshift/assets/middleware/rhoar-getting-started-nodejs/configmaps.png)

点击 ``app-config``  ConfigMap显示ConfigMap的详细信息:

![ConfigMaps](/openshift/assets/middleware/rhoar-getting-started-nodejs/configmap-detail.png)

要更改 ``message`` 的值，点击 _动作_ 按钮，选择 _编辑_ :

![ConfigMaps](/openshift/assets/middleware/rhoar-getting-started-nodejs/configmap-edit.png)

通过仔细更改现有文本来替换 ``message`` 的值。您可以使用 ``%s`` 作为名称的占位符
在问候语中包括:

![ConfigMaps](/openshift/assets/middleware/rhoar-getting-started-nodejs/configmap-edit-replace.png)

完成后，单击 _Save_ 保存更新的值。

 **2. 验证应用程序已更新:**

返回到应用程序并再次在 _Name_ 字段中键入您的名字。单击 **调用** 按钮验证返回的消息是否与你在ConfigMap中提供的相同:

![ConfigMaps](/openshift/assets/middleware/rhoar-getting-started-nodejs/configmap-verify.png)

## 恭喜你!

不需要修改任何一行代码，就可以使用OpenShift ConfigMaps更新应用程序的行为。