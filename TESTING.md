# Testing the GPU Scale-to-Zero Blueprint

Follow these steps to verify that the "Expert Glue" is working as expected.

## Prerequisites
1.  **Terraform Applied**: Ensure you have run `terraform apply` in the `terraform/` directory.
2.  **Kubeconfig**: Ensure your context is set to the new cluster.
    ```powershell
    aws eks update-kubeconfig --region us-west-2 --name ai-inference-cluster
    ```

## Step 1: Apply Karpenter Configuration
First, replace `${cluster_name}` in `gpu-nodepool.yaml` with your actual cluster name (e.g., `ai-inference-cluster`), then apply:

```powershell
kubectl apply -f k8s-manifests/gpu-nodepool.yaml
```

## Step 2: Deploy the AI Demo (at Scale 0)
Deploy the demo app. It won't trigger any node creation yet because `replicas` is set to `0`.

```powershell
kubectl apply -f k8s-manifests/inference-demo.yaml
```

## Step 3: Trigger Scale-Up (The Test)
Scale the deployment to 1 replica. Since it requests `nvidia.com/gpu: 1`, and no nodes currently have GPUs, Karpenter will be triggered.

```powershell
kubectl scale deployment ai-inference-demo --replicas=1
```

### What to watch for:
1.  **Check Karpenter Logs**:
    ```powershell
    kubectl logs -f -n karpenter -l app.kubernetes.io/name=karpenter
    ```
    *You should see logs like: "found provisionable pod(s)... creating node with 1 instance(s)..."*

2.  **Check Nodes**:
    ```powershell
    kubectl get nodes -w
    ```
    *Within 30-60 seconds, a new node should appear with a name like `ip-10-0-x-x.us-west-2.compute.internal`.*

3.  **Verify GPU Taints**:
    ```powershell
    kubectl get node <new-node-name> -o yaml | grep -A 5 taints
    ```
    *Verify it has the `nvidia.com/gpu:true:NoSchedule` taint.*

## Step 4: Trigger Scale-to-Zero
Once the pod is running, scale it back down to zero.

```powershell
kubectl scale deployment ai-inference-demo --replicas=0
```

### What to watch for:
1.  **Karpenter Consolidation**: Karpenter will realize the node is empty and underutilized.
2.  **Node Termination**: After a short "empty" period (usually ~30 seconds), Karpenter will de-provision the node.
    ```powershell
    kubectl get nodes -w
    ```
    *The GPU node should transition to `Ready,SchedulingDisabled` and then disappear.*

## Step 5: Cost Verification (Optional)
Check the AWS EC2 Console to confirm that the Spot instance was terminated. This confirms you are no longer being billed!
