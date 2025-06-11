# app/main.py
from app.connectors.csv_connector import CsvConnector
from app.core.reconciliation import reconcile_assets
from app.web.server import run_web_server

def main():
    """Main function to run the asset reconciliation."""
    print("AssetCon 啟動中，正在載入資料...")

    # 1. Initialize connectors for each data source
    servicenow_connector = CsvConnector("data/servicenow_cmdb.csv", "ServiceNow", "hostname")
    crowdstrike_connector = CsvConnector("data/crowdstrike_assets.csv", "CrowdStrike", "hostname")
    qualys_connector = CsvConnector("data/qualys_assets.csv", "Qualys", "hostname")
    guardicore_connector = CsvConnector("data/guardicore_assets.csv", "Guardicore", "hostname")
    
    # 2. Load data from all sources
    all_data = {
        "ServiceNow": servicenow_connector.load_assets(),
        "CrowdStrike": crowdstrike_connector.load_assets(),
        "Qualys": qualys_connector.load_assets(),
        "Guardicore": guardicore_connector.load_assets()
    }
    
    print("資料載入完成，開始進行比對...")
    
    # 3. Run the reconciliation engine
    try:
        reconciliation_report = reconcile_assets(all_data, master_source="ServiceNow")
    except ValueError as e:
        print(f"Error during reconciliation: {e}")
        return
        
    print("比對完成！準備啟動 Web UI...")
    
    # 4. Start the web server to display the report
    run_web_server(reconciliation_report)

if __name__ == "__main__":
    main()
