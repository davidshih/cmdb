# AssetCon - IT Asset Reconciliation System

AssetCon is a Configuration Management Database (CMDB) reconciliation tool that compares IT assets across multiple data sources to identify discrepancies.

## Overview

The system compares asset data from:
- ServiceNow CMDB (master source)
- CrowdStrike endpoint protection
- Qualys vulnerability scanner

It identifies:
- Assets missing from CrowdStrike or Qualys (potential security gaps)
- Orphaned assets in CrowdStrike or Qualys (not in CMDB)

## Requirements

- Python 3.7 or higher
- No external dependencies (uses Python standard library only)

## Setup

1. Ensure your CSV data files are in the `data/` directory:
   - `servicenow_cmdb.csv`
   - `crowdstrike_assets.csv`
   - `qualys_assets.csv`
   
   Each CSV must have a "hostname" column for asset identification.

2. Install Python dependencies (currently none required):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the reconciliation and start the web interface:

```bash
python -m app.main
```

The web interface will be available at: http://localhost:8089

## Project Structure

```
cmdb/
├── app/
│   ├── connectors/       # Data source connectors
│   │   ├── base_connector.py
│   │   └── csv_connector.py
│   ├── core/            # Core business logic
│   │   ├── models.py
│   │   └── reconciliation.py
│   ├── web/             # Web interface
│   │   ├── server.py
│   │   └── templates/
│   └── main.py          # Application entry point
├── data/                # CSV data files
└── tests/               # Test suite
```

## Data Format

CSV files should contain at minimum:
- `hostname`: Unique identifier for each asset

Additional columns will be preserved and displayed in the reconciliation report.