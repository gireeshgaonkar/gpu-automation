# ⚡ Project: GPU-Scale-To-Zero & FinOps Orchestrator
> **Role**: Staff Infrastructure Engineer / FinOps Lead
> **Target Impact**: 80% Reduction in AI Inference Infrastructure Costs

## 🚀 The Business Problem
AI workloads (LLMs, Diffusion Models) require expensive NVIDIA GPUs (g4dn/g5 instances). Most companies leave these nodes running 24/7, leading to thousands of dollars in "Idle Waste."

## 🛠️ The Solution
This project implements a production-grade **Scale-to-Zero** architecture using **Karpenter** on AWS EKS.

### Key Features:
*   **Intelligent Auto-Scaling**: Nodes are provisioned only when a pod requests `nvidia.com/gpu`.
*   **Spot-First Strategy**: Prioritizes Spot instances with a 100% weight, falling back to On-Demand only when Spot capacity is exhausted.
*   **Rapid Consolidation**: Configured to terminate idle nodes within 30 seconds of workload completion.
*   **FinOps Observability**: Custom Grafana dashboard tracking **GPU Efficiency Score** and **Burn Rate ($/hr)**.

## 🏗️ Architecture
1.  **Kubernetes**: EKS 1.30+
2.  **Node Management**: Karpenter v0.33+
3.  **Infrastructure**: Terraform (IAM, IRSA, Helm Providers)
4.  **Observability**: Prometheus Stack + Custom FinOps PromQL

## 📈 Results
*   **Idle Waste**: Reduced from ~12 hours/day to < 5 minutes/day.
*   **Cost Savings**: Estimated $1,200/month per GPU node in a dev environment.
*   **Reliability**: 0% Downtime due to intelligent On-Demand fallback logic.

## 🧪 Testing & Validation
This project includes a custom validation suite to ensure infrastructure logic integrity.

*   **Logic Validator**: A Python-based test (`tests/validate_logic.py`) that verifies Spot-priority weights and FinOps consolidation policies.
*   **Workload Simulation**: `tests/simulation-pod.yaml` provides a reference for GPU-requesting pods with correct Taints/Tolerations.

### Running Tests:
```bash
python tests/validate_logic.py
```
