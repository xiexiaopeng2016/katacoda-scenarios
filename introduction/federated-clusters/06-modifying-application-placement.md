此场景中的下一步是将应用程序从 ``cluster2`` 中删除，同时让它在 ``cluster1`` 中运行。为了执行该操作，我们将为 ``test-deployment`` 修补 ``FederatedDeployment`` 的放置策略，这样它将只在 ``cluster1`` 上存在:

``oc --context=cluster1 -n test-namespace patch federateddeployment test-deployment --type=merge -p '{"spec":{"placement":{"clusters": [{"name":"cluster1"}]}}}'``{{execute HOST1}}

现在我们应该看到我们的应用程序部署撤离 ``cluster2`` :


```
for cluster in cluster1 cluster2; do
    echo ------------ ${cluster} deployments ------------
    oc --context=${cluster} -n test-namespace get deployments -l app=nginx
done
```{{execute HOST1}}

If we wanted to deploy our application to `cluster2` again, we could patch the `FederatedDeployment` placement policy again:

``oc --context=cluster1 -n test-namespace patch federateddeployment test-deployment --type=merge -p '{"spec":{"placement":{"clusters": [{"name":"cluster1"}, {"name":"cluster2"}]}}}'``{{execute HOST1}}

After a while, we should see our application deployment deployed on `cluster2`:

```
for cluster in cluster1 cluster2; do
    echo ------------ ${cluster} deployments ------------
    oc --context=${cluster} -n test-namespace get deployments -l app=nginx
done
```{{execute HOST1}}
