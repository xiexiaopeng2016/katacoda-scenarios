## 联合部署

这个对象指示KubeFed控制面板联合一个名为 ``test-deployment`` 的部署。

对象中的放置策略指示KubeFed控制面板将我们的 ``test-deployment`` 放置在 ``cluster1`` 和 ``cluster2`` 上。

对象中的overrides策略指示KubeFed控制面板覆盖 ``test-deployment`` 的副本数量，从默认的3(在FederatedDeployment模板中定义)覆盖到 ``cluster2`` 上的5。

```yaml
apiVersion: types.federation.k8s.io/v1alpha1
kind: FederatedDeployment
metadata:
  name: test-deployment
  namespace: test-namespace
spec:
  template:
    metadata:
      labels:
        app: nginx
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - image: nginx
            name: nginx
  placement:
    clusters:
    - name: cluster1
    - name: cluster2
  overrides:
  - clusterName: cluster2
    clusterOverrides:
    - path: "/spec/replicas"
      value: 5
```