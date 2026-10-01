from difflib import SequenceMatcher
from database import supabase

def calculate_match_score(finding_A, finding_B):
    score = 0

    if finding_A["host"] == finding_B["host"]:
        score += 1

    if finding_A["port"] is not None:
        if finding_A["port"] == finding_B["port"]:
            score += 0.3

    if finding_A["cve_id"] is not None:
        if finding_A["cve_id"] == finding_B["cve_id"]:
            score += 0.5

    if finding_A["endpoint"] is not None:
        if finding_A["endpoint"] == finding_B["endpoint"]:
            score += 0.5

    similarity = SequenceMatcher(
        None,
        finding_A["title"].lower(),
        finding_B["title"].lower()
    ).ratio()

    if similarity > 0.7:
        score += 0.2

    return score

def is_duplicate(score):
    if score >= 1.5 :
        return True
    else :
        return False
    
def get_asset_id(user_id, host):
    response = (
        supabase
        .table("assets")
        .select("id")
        .eq("user_id", user_id)
        .eq("host", host)
        .execute()
    )
    if not response.data:
        return None

    return response.data[0]["id"]
    
    
def get_existing_findings(asset_id):
    response = (
        supabase
        .table("findings")
        .select("*, scans!inner(asset_id)")
        .eq("scans.asset_id", asset_id)
        .execute()
    )

    if not response.data:
        return []

    return response.data

    
    
def check_duplicate_findings(finding,user_id):
    asset_id = get_asset_id(user_id,finding["host"])
    if asset_id is None :
        return False
    existing_findings = get_existing_findings(asset_id)

    for existing_finding in existing_findings:
        score = calculate_match_score(
            finding,
            existing_finding
        )

        if is_duplicate(score):
            return True

    return False


if __name__ == "__main__":

    finding_a = {
        "host": "192.168.1.10",
        "port": 22,
        "title": "ssh",
        "cve_id": None
    }

    finding_b = {
        "host": "192.168.1.10",
        "port": 22,
        "title": "ssh",
        "cve_id": None
    }

    score = calculate_match_score(finding_a, finding_b)

    print("Score:", score)
    print("Duplicate:", is_duplicate(score))



'''
user_id + host
      ↓
 get_asset_id()
      ↓
 asset_id
      ↓
get_existing_findings()
      ↓
existing findings
      ↓
calculate_match_score()
      ↓
is_duplicate()
      ↓
True / False
'''