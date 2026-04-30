import yaml
import sys

def validate_karpenter_logic(file_path):
    print(f"[INFO] Validating Business Logic for: {file_path}")
    try:
        with open(file_path, 'r') as f:
            docs = list(yaml.load_all(f, Loader=yaml.FullLoader))
        
        spot_pool = next((d for d in docs if d.get('metadata', {}).get('name') == 'gpu-spot-ai-research'), None)
        od_pool = next((d for d in docs if d.get('metadata', {}).get('name') == 'gpu-on-demand-fallback'), None)

        if not spot_pool or not od_pool:
            print("[ERROR] Could not find both Spot and On-Demand pools.")
            return False

        # Logic Check 1: Spot Weight vs On-Demand Weight
        spot_weight = spot_pool['spec'].get('weight', 0)
        od_weight = od_pool['spec'].get('weight', 0)
        
        if spot_weight <= od_weight:
            print(f"[FAIL] LOGIC ERROR: Spot weight ({spot_weight}) must be higher than On-Demand ({od_weight}) to save costs!")
            return False
        else:
            print(f"[PASS] Spot priority ({spot_weight}) is correctly higher than On-Demand ({od_weight}).")

        # Logic Check 2: Consolidation Policy
        if spot_pool['spec']['disruption'].get('consolidationPolicy') != 'WhenUnderutilized':
            print("[FAIL] LOGIC ERROR: Spot pool should use 'WhenUnderutilized' for maximum savings.")
            return False
        else:
            print("[PASS] Consolidation policy is optimized for FinOps.")

        return True

    except Exception as e:
        print(f"[ERROR] FILE ERROR: {e}")
        return False

if __name__ == "__main__":
    success = validate_karpenter_logic('k8s-manifests/gpu-nodepool.yaml')
    if not success:
        sys.exit(1)
    print("[SUCCESS] All Business Logic Tests Passed!")
