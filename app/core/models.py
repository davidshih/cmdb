# app/core/models.py
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Asset:
    """Represents a single asset from any source."""
    identifier: str  # The common key, e.g., hostname
    source: str      # Where this data came from (e.g., 'ServiceNow', 'CrowdStrike')
    details: Dict[str, Any] = field(default_factory=dict)
