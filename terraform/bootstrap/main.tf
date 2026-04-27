# This is the "Expert Glue" for bootstrapping OIDC. 
# Run this once using Access Keys to eliminate the need for them forever.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "us-west-2"
}

variable "github_repo" {
  description = "The GitHub repository in 'owner/repo' format"
  type        = string
}

# 1. Create the OIDC Provider for GitHub
module "iam_github_oidc_provider" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-github-oidc-provider"
  version = "~> 5.30"
}

# 2. Create the Role that GitHub Actions will assume
module "iam_github_oidc_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-github-oidc-role"
  version = "~> 5.30"

  name = "github-actions-eks-deployer"

  # Trust policy: Only allow your specific repo to assume this role
  subjects = ["${var.github_repo}:*"]

  policies = {
    AdministratorAccess = "arn:aws:iam::aws:policy/AdministratorAccess" # For demo purposes, scope this down in production
  }
}

output "role_arn" {
  description = "The ARN of the role for GitHub Actions to assume"
  value       = module.iam_github_oidc_role.arn
}
