# app/connectors/csv_connector.py
import csv
from typing import List
from .base_connector import BaseConnector
from app.core.models import Asset

class CsvConnector(BaseConnector):
    """Connector to load assets from a CSV file."""
    
    def __init__(self, file_path: str, source_name: str, identifier_column: str):
        self.file_path = file_path
        self.source_name = source_name
        self.identifier_column = identifier_column

    def load_assets(self) -> List[Asset]:
        assets = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    identifier = row.get(self.identifier_column)
                    if identifier:
                        # Remove identifier from details to avoid redundancy
                        details = {k: v for k, v in row.items() if k != self.identifier_column}
                        assets.append(Asset(
                            identifier=identifier,
                            source=self.source_name,
                            details=details
                        ))
        except FileNotFoundError:
            print(f"Warning: File not found at {self.file_path}. Skipping source {self.source_name}.")
            return []
            
        return assets
