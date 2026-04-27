# AI-Inference K8s Cold-Start Blueprint
**High-Stakes Automation: GPU Scale-to-Zero on AWS EKS**

## The Problem
Running GPU instances (`g4dn`, `g5`, `p3`) 24/7 is prohibitively expensive for startups. Idle GPUs can waste thousands of dollars per month.

## The Solution (The "Expert Glue")
This blueprint uses **Karpenter** to manage **GPU Spot Instances** with a focus on "Scale-to-Zero."

### Key Features:
1.  **Spot-First Strategy**: Automatically prefers Spot instances to save ~70% on compute costs.
2.  **Hardened Foundation**: Deploys into a private-only VPC with NAT gateways and IAM Least Privilege roles (SOC2-ready).
3.  **Cold-Start Optimization**: Uses Karpenter's rapid provisioning to spin up GPU nodes in < 60 seconds from an idle state.
4.  **Automatic Consolidation**: When an inference pod is finished and the deployment scales down, Karpenter immediately terminates the node to stop billing.
5.  **Interruption Handling**: Integrated with AWS SQS/EventBridge to handle Spot terminations gracefully by migrating workloads before the node is reclaimed.

## Components
- `terraform/`: VPC, EKS, and Karpenter Controller provisioning.
- `k8s-manifests/`:
    - `gpu-nodepool.yaml`: The logic for finding and scaling GPU nodes.
    - `inference-demo.yaml`: A test deployment to verify the scale-up/down behavior.
- `.github/workflows/deploy.yml`: Fully automated CI/CD pipeline using OIDC and `envsubst`.

## How to Sell This
This isn't just code; it's a **Cost Reduction Strategy**. 
- **Target**: AI/ML startups using EKS.
- **Value Prop**: "Reduce your AI infra bill by 70% while maintaining enterprise-grade security."
