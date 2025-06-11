# app/core/reconciliation.py
from typing import Dict, List, Set
from app.core.models import Asset

def reconcile_assets(data: Dict[str, List[Asset]], master_source: str) -> Dict:
    """
    Compares asset lists from various sources against a master source.

    Returns a dictionary with reconciliation results.
    """
    if master_source not in data or not data[master_source]:
        raise ValueError(f"Master source '{master_source}' not found or is empty.")

    # Create lookup dictionaries for detailed comparisons
    master_assets = {asset.identifier: asset for asset in data[master_source]}
    master_identifiers: Set[str] = set(master_assets.keys())
    
    report = {
        "summary": {
            "master_source": master_source,
            "total_master_assets": len(master_identifiers)
        },
        "details": {},
        "assets": {}  # Store detailed asset information
    }

    # Store master assets details
    report["assets"][master_source] = {
        asset.identifier: asset.details for asset in data[master_source]
    }

    # Compare each source against the master
    for source_name, assets in data.items():
        if source_name == master_source:
            continue
        
        # Create lookup for source assets
        source_assets = {asset.identifier: asset for asset in assets}
        source_identifiers: Set[str] = set(source_assets.keys())
        
        # Store source assets details
        report["assets"][source_name] = {
            asset.identifier: asset.details for asset in assets
        }
        
        missing_in_source = list(sorted(master_identifiers - source_identifiers))
        found_only_in_source = list(sorted(source_identifiers - master_identifiers))
        matched_assets = list(sorted(master_identifiers & source_identifiers))
        
        # Build detailed comparison data
        missing_details = []
        for asset_id in missing_in_source:
            missing_details.append({
                "identifier": asset_id,
                "details": master_assets[asset_id].details
            })
        
        orphaned_details = []
        for asset_id in found_only_in_source:
            orphaned_details.append({
                "identifier": asset_id,
                "details": source_assets[asset_id].details
            })
        
        report["details"][source_name] = {
            "assets_found": len(source_identifiers),
            "missing_from_master": missing_in_source,
            "count_missing_from_master": len(missing_in_source),
            "found_only_in_source": found_only_in_source,
            "count_found_only_in_source": len(found_only_in_source),
            "matched_assets": matched_assets,
            "count_matched": len(matched_assets),
            # Enhanced details for better diff view
            "missing_details": missing_details,
            "orphaned_details": orphaned_details
        }
        
    return report
