#!/bin/bash
set -e

echo "⚡ Deploying Kube-Prometheus-Stack (Prometheus + Grafana)..."

# Add the prometheus-community helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring || true

# Install the prometheus stack using Helm
# We enable sidecar dashboards so Grafana auto-discovers our ConfigMap
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.sidecar.dashboards.enabled=true \
  --set grafana.sidecar.dashboards.label=grafana_dashboard \
  --set grafana.sidecar.dashboards.labelValue="1"

echo "✅ Prometheus Stack Installed!"

echo "⚡ Applying Custom GPU Cost Dashboard..."
kubectl apply -f k8s-manifests/grafana-cost-dashboard.yaml

echo "=========================================================="
echo "🎉 Deployment Complete!"
echo ""
echo "To view your dashboards, run the following port-forward command:"
echo "kubectl port-forward svc/prometheus-grafana 8080:80 -n monitoring"
echo ""
echo "Then open: http://localhost:8080"
echo "Login Credentials:"
echo "Username: admin"
echo "Password: prom-operator"
echo "=========================================================="
