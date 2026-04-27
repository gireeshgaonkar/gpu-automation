# 🚀 GPU Scale-to-Zero Blueprint
### High-Stakes Automation for AI/ML Infrastructure on AWS EKS

[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)

---

## 💡 The Problem
AI startups often face a "GPU Tax." Keeping high-performance GPU instances (`g4dn`, `g5`, `p3`) running 24/7 is a fast way to burn through venture capital. Even when no inference is happening, idle nodes cost thousands of dollars per month.

## 🛠️ The Solution (The "Expert Glue")
This repository provides an **Opinionated, Production-Ready Blueprint** that automates the lifecycle of GPU nodes on Amazon EKS using **Karpenter**.

### Core Value Propositions:
*   **💰 70% Cost Reduction**: Prefers Spot instances for GPU workloads automatically.
*   **📉 Scale-to-Zero**: Terminated GPU nodes the moment they go idle. No idle waste.
*   **🔒 SOC2-Hardened**: Deploys into a private-only VPC with IAM Least Privilege and OIDC authentication.
*   **⚡ Rapid Provisioning**: Spin up fresh GPU nodes in < 60 seconds when a new request arrives.
*   **📊 Cost Visibility**: Built-in Python script to report real-time savings directly in your CI/CD logs.

---

## 🏗️ Architecture
1.  **VPC Foundation**: Hardened network with private subnets and NAT gateways.
2.  **EKS Cluster**: Modern Kubernetes (1.30+) with OIDC enabled.
3.  **Karpenter Controller**: Handles intelligent, just-in-time node provisioning.
4.  **GPU NodePool**: Specific logic to find the cheapest GPU Spot instances across multiple families (`g4dn`, `g5`, `p3`).

---

## 🚦 Quick Start

### 1. Initial Setup (The "Bootstrap")
This repo uses **GitHub OIDC** for secure, secretless authentication. To set this up:
1.  Add your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to GitHub Secrets.
2.  Run the **"Bootstrap OIDC"** workflow manually from the Actions tab.
3.  Copy the resulting **Role ARN** to a GitHub Secret named `AWS_ROLE_ARN`.
4.  **Delete your static keys!** The pipeline now uses secure, short-lived tokens.

### 2. Deployment
Simply push to the `main` branch. The GitHub Action will:
1.  Provision/Update your EKS Infrastructure via Terraform.
2.  Configure Karpenter NodePools.
3.  Run a **Cost Savings Report**.

### 3. Verification
Scale the demo app to see the magic happen:
```powershell
# Watch nodes spin up
kubectl scale deployment ai-inference-demo --replicas=1

# Watch nodes disappear
kubectl scale deployment ai-inference-demo --replicas=0
```

---

## 📈 Cost Watcher Report
The included [cost-watcher.py](./scripts/cost-watcher.py) runs automatically in the pipeline and provides output like this:

```text
✅ Active Node: g4dn.xlarge (Spot) | Cost: $0.158/hr (Saved $0.368/hr)
------------------------------------------------------------
Current Burn Rate:  $0.158/hr
Potential Burn:     $0.526/hr (Without Scale-to-Zero/Spot)
Estimated Savings:  $0.368/hr
Projected Monthly:  $264.96/month 💰
------------------------------------------------------------
```

---

## 👨‍💻 Author
**Gireesh Gaonkar**
*DevOps & Cloud Infrastructure Architect*

---
> [!IMPORTANT]
> This is a **High-Stakes Automation Blueprint**. It is designed for production reliability and cost efficiency.
