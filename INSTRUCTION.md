# Kubernetes ToDo Application Deployment Guide

## 1. Applying Manifests

To deploy all Kubernetes resources, navigate to the `.infrastructure` directory and run:

```bash
kubectl apply -f namespace.yml && \
kubectl apply -f todoapp-pod.yml && \
kubectl apply -f busybox.yml
```

## 2. Testing the ToDo Application (Local Port-Forward)

To test the application locally:

```bash
(kubectl port-forward pod/todoapp 8000:8000 &>/dev/null & PORT_FORWARD_PID=$!; \
sleep 3; \
curl -fs localhost:8000/api/ready || echo '{"error": "curl failed"}'; \
kill $PORT_FORWARD_PID) 2>/dev/null
```

**Expected Output:**
```json
{"status": "READY"}
```


## 3. Testing from Within the Cluster

To test using the busybox container:

```bash
kubectl exec -n todoapp busybox -- \
  curl -s http://$(kubectl get pod -n todoapp -l app=todoapp -o jsonpath='{.items[0].status.podIP}'):8000/api/ready
```

**Expected Output:**
```json
{"status": "READY"}
```
