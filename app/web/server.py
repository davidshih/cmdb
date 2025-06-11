# app/web/server.py
import http.server
import socketserver
import datetime
from typing import Dict

PORT = 8089

class ReconciliationHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    reconciliation_data = {} # Class variable to hold data

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Generate the HTML content
            html = self.generate_html_report()
            self.wfile.write(bytes(html, "utf8"))
        else:
            # Fallback to serving files if needed (e.g., CSS), but we embed CSS for simplicity
            super().do_GET()
            
    def generate_html_report(self) -> str:
        import json
        
        # Try new template first, fallback to old one
        template_path = "app/web/templates/sankey.html"
        try:
            with open(template_path, "r") as f:
                template = f.read()
        except FileNotFoundError:
            # Fallback to old template
            try:
                with open("app/web/templates/index.html", "r") as f:
                    template = f.read()
                    return self._generate_old_html_report(template)
            except FileNotFoundError:
                return "<html><body><h1>Error: Template not found.</h1></body></html>"
        
        # Inject the reconciliation data as JSON
        data_json = json.dumps(self.reconciliation_data, indent=2)
        final_html = template.replace('<!-- RECONCILIATION_DATA -->', data_json)
        
        return final_html
    
    def _generate_old_html_report(self, template: str) -> str:
        """Legacy HTML report generation for backward compatibility"""
        report = self.reconciliation_data
        summary = report.get("summary", {})
        template = template.replace('<span id="generated-on"></span>', f'<span id="generated-on">{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>')
        template = template.replace('<strong id="master-source"></strong>', f'<strong id="master-source">{summary.get("master_source", "N/A")}</strong>')
        template = template.replace('<strong id="total-master-assets"></strong>', f'<strong id="total-master-assets">{str(summary.get("total_master_assets", 0))}</strong>')
        
        # Build detailed reports using Bootstrap Accordion
        details_html = ""
        item_id = 0
        for source, detail in report.get("details", {}).items():
            item_id += 1
            details_html += f'''
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading{item_id}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{item_id}" aria-expanded="false" aria-controls="collapse{item_id}">
                        來源: {source} (找到: {detail["assets_found"]})
                    </button>
                </h2>
                <div id="collapse{item_id}" class="accordion-collapse collapse" aria-labelledby="heading{item_id}" data-bs-parent="#detailsAccordion">
                    <div class="accordion-body">
                        <h4 class="text-danger">在 CMDB 中但在此來源中缺失的資產 ({detail["count_missing_from_master"]}):</h4>
                        <ul class="list-group mb-3">'''
            if detail["missing_from_master"]:
                details_html += "".join([f'<li class="list-group-item missing">{asset}</li>' for asset in detail["missing_from_master"]])
            else:
                details_html += '<li class="list-group-item">無。做得好！</li>'
            details_html += f'''
                        </ul>
                        <h4 class="text-warning">僅在此來源中找到的資產 (孤立資產) ({detail["count_found_only_in_source"]}):</h4>
                        <ul class="list-group">'''
            if detail["found_only_in_source"]:
                details_html += "".join([f'<li class="list-group-item orphan">{asset}</li>' for asset in detail["found_only_in_source"]])
            else:
                details_html += '<li class="list-group-item">無。</li>'
            details_html += f'''
                        </ul>
                    </div>
                </div>
            </div>'''
            
        final_html = template.replace('<!-- Detailed reports will be inserted here by server.py -->', details_html)
        return final_html

def run_web_server(report_data: Dict):
    """Starts the web server with the provided report data."""
    ReconciliationHttpRequestHandler.reconciliation_data = report_data
    with socketserver.TCPServer(("", PORT), ReconciliationHttpRequestHandler) as httpd:
        print(f"鄉民們，上車啦！伺服器開在 http://localhost:{PORT}")
        print("按 Ctrl+C 結束...")
        httpd.serve_forever()
