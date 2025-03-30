1. Instructions on how to apply all manifests
cd to .infrastructure and run this command
kubectl apply -f namespace.yml && kubectl apply -f todoapp-pod.yml

2. Instructions on how to test ToDo application using the port-forward command
run this command 
(kubectl port-forward pod/todoapp 8000:8000 &>/dev/null & PORT_FORWARD_PID=$!; sleep 3; curl -fs localhost:8000/api/ready || echo '{"error": "curl failed"}'; kill $PORT_FORWARD_PID) 2>/dev/null

The result should be "{"status": "READY"}".
If you see {"error": "curl failed"} something went wrong.

3. Instructions on how to test the application using the busyboxplus:curl container
Run this command
kubectl exec -n todoapp busybox -- curl -s http://$(kubectl get pod -n todoapp -l app=todoapp -o jsonpath='{.items[0].status.podIP}'):8000/api/ready

The result should be "{"status": "READY"}".
