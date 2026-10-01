from urllib.parse import urlparse

def normalize_nmap_findings(results):
    findings = []
    for result in results :
        if result["state"] == "open":
            finding = {
                "host" : result["host"],
                "port" : result["port"],
                "title" : result["service"],
                "description": None,
                "severity": None,
                "cve_id": None,
                "endpoint": None
            }
            findings.append(finding)
            
    return findings

def normalize_zap_findings(results):
    findings = []
    severity_map = {
        "0": "Informational",
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }
    
    for result in results :
        url = result["url"]
        parsed_host = urlparse(url)
        host = parsed_host.hostname
        port = parsed_host.port
        severity = severity_map[result["severity"]]
        finding = {
            "host" : host,
            "port" : port,
            "title" : result["title"],
            "description": result["description"],
            "severity": severity,
            "cve_id": None,
            "endpoint": result["endpoint"]
            }
        findings.append(finding)
            
    return findings
