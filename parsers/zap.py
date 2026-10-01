import xml.etree.ElementTree as ET
def parse_zap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    get_sites = root.findall("site")
    parsed_results = []

    for s in get_sites:
        url = s.get("name")

        if url is None:
            continue

        get_alerts = s.find("alerts")

        if get_alerts is None:
            continue

        alert_items = get_alerts.findall("alertitem")

        for item in alert_items:
            get_alert = item.find("alert")

            if get_alert is None:
                continue

            title = get_alert.text

            if title is None:
                continue

            get_riskcode = item.find("riskcode")

            if get_riskcode is None:
                severity = None
            else:
                severity = get_riskcode.text

            get_description = item.find("desc")

            if get_description is None:
                description = None
            else:
                description = get_description.text

            get_instances = item.find("instances")

            if get_instances is None:
                continue

            get_all_instance = get_instances.findall("instance")

            for instance in get_all_instance:
                get_uri = instance.find("uri")

                if get_uri is None:
                    endpoint = None
                else:
                    endpoint = get_uri.text

                parsed_result = {
                    "url": url,
                    "title": title,
                    "severity": severity,
                    "description": description,
                    "endpoint": endpoint
                }

                parsed_results.append(parsed_result)

    return parsed_results










# import xml.etree.ElementTree as ET

# def parse_zap(file_path):
#     tree = ET.parse(file_path)
#     root = tree.getroot()
    
#     get_sites = root.findall("site")
#     parsed_results = []
    
#     for s in get_sites:
#         url = s.get("name")
        
#         get_alerts = s.find("alerts")
#         alert_items = get_alerts.findall("alertitem")
#         for item in alert_items :
#             get_alert = item.find("alert")
#             title = get_alert.text
            
#             get_riskcode = item.find("riskcode")
#             severity = get_riskcode.text
            
#             get_description = item.find("desc")
#             description = get_description.text
            
#             get_instances = item.find("instances")
#             get_all_instance = get_instances.findall("instance")
#             for instance in get_all_instance :
#                 get_uri = instance.find("uri")
#                 endpoint = get_uri.text
                
#                 parsed_result = {
#                     "url" : url,
#                     "title" : title,
#                     "severity" : severity,
#                     "description" : description ,
#                     "endpoint" : endpoint
#                 }
#                 parsed_results.append(parsed_result)
                
#     return parsed_results
    
            

    
