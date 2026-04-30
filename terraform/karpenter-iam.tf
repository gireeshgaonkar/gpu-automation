# STAFF-LEVEL TERRAFORM MODULE: KARPENTER AI-OPS
# Purpose: Provisioning the IAM and NodeClasses for GPU Spot Clusters

module "karpenter" {
  source = "terraform-aws-modules/eks/aws//modules/karpenter"

  cluster_name = var.cluster_name

  enable_irsa                     = true
  irsa_oidc_provider_arn          = module.eks.oidc_provider_arn
  irsa_namespace_service_accounts = ["karpenter:karpenter"]

  # Staff Tip: Always use specific tags for FinOps tracking
  tags = {
    Environment = "Production"
    CostCenter  = "AI-Research"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_instance_profile" "karpenter" {
  name = "KarpenterNodeInstanceProfile-${var.cluster_name}"
  role = module.eks.eks_managed_node_groups["gpu_nodes"].iam_role_name
}

# Helm Provider for Karpenter
resource "helm_release" "karpenter" {
  namespace        = "karpenter"
  create_namespace = true

  name       = "karpenter"
  repository = "https://charts.karpenter.sh"
  chart      = "karpenter"
  version    = "v0.33.0"

  set {
    name  = "settings.aws.clusterName"
    value = var.cluster_name
  }

  set {
    name  = "settings.aws.defaultInstanceProfile"
    value = aws_iam_instance_profile.karpenter.name
  }
}
