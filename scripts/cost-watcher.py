import boto3
import json
from kubernetes import client, config
from datetime import datetime

# Simple pricing map for popular GPU instances (On-Demand prices)
# In a real tool, we would use the AWS Pricing API
PRICING = {
    "g4dn.xlarge": 0.526,
    "g4dn.2xlarge": 0.752,
    "g5.xlarge": 1.006,
    "p3.2xlarge": 3.06,
}

SPOT_DISCOUNT = 0.70  # Typical 70% discount for Spot

def get_active_nodes():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1 = client.CoreV1Api()
    nodes = v1.list_node().items
    return nodes

def calculate_savings():
    nodes = get_active_nodes()
    total_on_demand_hourly = 0
    total_spot_hourly = 0
    gpu_nodes_count = 0

    print(f"--- GPU Scale-to-Zero Cost Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    
    for node in nodes:
        labels = node.metadata.labels
        instance_type = labels.get("node.kubernetes.io/instance-type")
        capacity_type = labels.get("karpenter.sh/capacity-type")
        
        # Check if it's a GPU node (based on our NodePool labels or instance family)
        if instance_type in PRICING:
            gpu_nodes_count += 1
            hourly_rate = PRICING[instance_type]
            
            if capacity_type == "spot":
                cost = hourly_rate * (1 - SPOT_DISCOUNT)
                total_spot_hourly += cost
                total_on_demand_hourly += hourly_rate
                print(f"✅ Active Node: {instance_type} (Spot) | Cost: ${cost:.3f}/hr (Saved ${hourly_rate - cost:.3f}/hr)")
            else:
                total_spot_hourly += hourly_rate
                total_on_demand_hourly += hourly_rate
                print(f"⚠️ Active Node: {instance_type} (On-Demand) | Cost: ${hourly_rate:.3f}/hr")

    # Scale-to-Zero logic: If we have 0 nodes, our "Burn" is 0. 
    # Without this blueprint, a startup might keep 1 node running 24/7.
    baseline_waste = PRICING["g4dn.xlarge"] # Assume 1 idle g4dn.xlarge without this blueprint
    
    current_burn = total_spot_hourly
    potential_burn = total_on_demand_hourly if gpu_nodes_count > 0 else baseline_waste
    
    hourly_savings = max(0, potential_burn - current_burn)
    monthly_savings = hourly_savings * 24 * 30

    print("-" * 60)
    print(f"Current Burn Rate:  ${current_burn:.3f}/hr")
    print(f"Potential Burn:     ${potential_burn:.3f}/hr (Without Scale-to-Zero/Spot)")
    print(f"Estimated Savings:  ${hourly_savings:.3f}/hr")
    print(f"Projected Monthly:  ${monthly_savings:.2f}/month 💰")
    print("-" * 60)

if __name__ == "__main__":
    calculate_savings()
