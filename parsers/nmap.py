import xml.etree.ElementTree as ET


def parse_nmap(file_path): 
    tree = ET.parse(file_path) # made the file content tree
    root = tree.getroot()  # got the root i.e nmaprun
    
    hosts = root.findall("host") # we have multiple hosts i.e nmaprun/host(n)
    parsed_results = [] 
    for h in hosts: # 1 host at a time
        get_addr = h.find("address") # because we have only 1 address object
        if get_addr is  None :
            continue
        ip = get_addr.get("addr")
        if ip is None :
            continue
        get_ports = h.find("ports") # we have 1 ports object
        if get_ports is None  :
            continue
        ports = get_ports.findall("port") # but inside it we have mutliple ports

        for p in ports: # 1 port at a time
            port_id = p.get("portid")
            if port_id is None :
                continue
            get_state = p.find("state")
            if get_state is None :
                continue
            state = get_state.get("state")
            if state is None :
                continue
            get_service = p.find("service")
            if get_service is None :
                continue
            service = get_service.get("name")
            if service is None :
                continue
            
            parsed_result = {
                    "host": ip,
                    "port": int(port_id),
                    "state": state,
                    "service": service
                }
            parsed_results.append(parsed_result)
            
    return parsed_results