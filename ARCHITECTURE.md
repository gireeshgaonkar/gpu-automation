# Architecture Deep Dive

This document explains the "Expert Glue" that makes this blueprint work.

## 1. The Provisioning Flow
When a pod requesting `nvidia.com/gpu` is created:
1.  **K8s Scheduler** marks the pod as `Pending` because no existing node satisfies the resource request.
2.  **Karpenter** intercepts the `Pending` pod and checks the `NodePool` configuration.
3.  **Instance Selection**: Karpenter queries the AWS EC2 Fleet API to find the cheapest available GPU instance type in the allowed families (`g4dn`, `g5`, `p3`) that satisfies the pod's requirements.
4.  **Just-in-Time Provisioning**: Karpenter creates a new EC2 instance and injects the NVIDIA device plugin configuration via the `EC2NodeClass`.

## 2. Cost Optimization Logic
We use a **Spot-First** strategy.
*   **Consolidation**: The `consolidationPolicy: WhenUnderutilized` tells Karpenter to constantly monitor if pods can be moved to cheaper nodes or if a node can be deleted entirely.
*   **Taints & Tolerations**: GPU nodes are created with the `nvidia.com/gpu:true:NoSchedule` taint. This ensures that only AI workloads (which have the matching toleration) land on these expensive nodes. Your standard `nginx` or `frontend` pods will never accidentally cost you GPU money.

## 3. Security (SOC2 Compliance)
*   **Private-Only VPC**: No nodes are directly exposed to the internet. All egress is handled via NAT Gateways.
*   **OIDC (IAM Roles for Service Accounts)**: The Karpenter controller and the AI workloads use IRSA to interact with AWS APIs. This eliminates the need for hardcoded AWS keys inside the cluster.
*   **Encrypted EBS**: All volumes created by Karpenter are encrypted at rest by default (`encrypted: true` in `EC2NodeClass`).

## 4. Disaster Recovery
*   **Spot Interruption Handling**: The blueprint includes an SQS queue that listens for "Spot Termination Notices" from AWS. Karpenter will automatically "cordon and drain" a node 2 minutes before AWS reclaims it, giving your inference pods time to finish or migrate.
