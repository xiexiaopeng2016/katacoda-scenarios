现在我们已经准备好修改我们的应用程序以使用ConfigMaps了!

在示例应用程序中，这是返回给服务调用者的硬编码消息:

```javascript
let message = "Default hard-coded greeting: Hello, %s!";
```

我们将定期检索ConfigMap并覆盖 ``message`` 的值，从而覆盖这个值。

 **1. 添加时间间隔检索配置**

在``app.js``{{open}}中添加一个新的代码块，该代码块每2秒执行一次，检索消息值并覆盖
变量。点击下面的 **复制到编辑器** 按钮，将这段代码放到``app.js``{{open}}中:

<pre class="file" data-filename="app.js" data-target="insert" data-marker="// TODO: Periodic check for config map update">
setInterval(() => {
  retrieveConfigMap().then((config) => {
    if (!config) {
      message = null;
      return;
    }

    if (JSON.stringify(config) !== JSON.stringify(configMap)) {
      configMap = config;
      message = config.message;
    }
  }).catch((err) => {
    console.log("error: ", err);
  });
}, 2000);

</pre>

我们使用 [Promise链](https://javascript.info/promise-chaining) 来高效写入但可读的异步方法调用链来检索ConfigMap。

上面的方法调用 ``setInterval()`` (Node.js的间隔计时器)来周期性地调用 ``retrieveConfigMap()`` 返回一个 _promise_ 对象，一旦完成，它将返回名为 ``config`` 的ConfigMap对象，并将其传递给回调函数以覆盖该值 ``message`` 。为了本示例的目的，我们捕获并忽略错误。

现在我们有了更新值的逻辑，我们需要实现缺失的 ``retrieveConfigMap()`` 方法
将需要返回一个 _promise_ 来调用OpenShift并检索ConfigMap内容本身。

 **2. 添加ConfigMap检索逻辑**

点击下面的 **复制到编辑器** 来实现``app.js``{{open}}中的逻辑

<pre class="file" data-filename="app.js" data-target="insert" data-marker="// TODO: Retrieve ConfigMap">
// Find the Config Map
const openshiftRestClient = require('openshift-rest-client').OpenshiftClient;
const config = require('openshift-rest-client').config;
const customConfig = config.getInCluster();

async function retrieveConfigMap() {
  const client = await openshiftRestClient({config: customConfig});
  const configmap = await client.api.v1.namespaces('example').configmaps('app-config').get();
  return jsyaml.safeLoad(configmap.body.data['app-config.yml']);
}
</pre>

在这段代码中，我们返回了另一个 _promise_ (使用javascript的 [异步函数](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) )，它将负责使用 [openshift-rest-client](https://www.npmjs.com/package/openshift-rest-client) 模块来调用OpenShift REST API并检索ConfigMap。

承诺和异步的使用可能需要一些时间来适应，但最终它会产生有序且定义良好的从OpenShift检索ConfigMap的过程，将其解析为javascript友好的JSON对象，并使用它来覆盖我们的 ``message`` 变量的值，以便我们可以从外部控制它的值，而不需要在应用程序代码。最后一个每2秒被调用的链看起来像:

 ``openshiftRestClient -> retrieve ConfigMap using .find('app-config') -> convert yaml to json ->  override message value``

有了我们的新逻辑，我们现在可以在OpenShift中创建实际的ConfigMap，它将包含逻辑访问的配置值。