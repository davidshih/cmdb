# app/connectors/base_connector.py
import abc
from typing import List
from app.core.models import Asset

class BaseConnector(abc.ABC):
    """Abstract Base Class for all data source connectors."""
    
    @abc.abstractmethod
    def load_assets(self) -> List[Asset]:
        """Load assets from the source and return a list of Asset objects."""
        pass
