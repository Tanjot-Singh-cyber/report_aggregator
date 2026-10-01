from services.deduplicate import calculate_match_score, is_duplicate
from database import supabase



def find_matching_finding(target_finding, candidate_findings):
    for candidate_finding in candidate_findings:
        score = calculate_match_score(
            target_finding,
            candidate_finding
        )

        if is_duplicate(score):
            return candidate_finding

    return None



def get_previous_scan(asset_id, current_scan_id):
    response = (
        supabase
        .table("scans")
        .select("*")
        .eq("asset_id", asset_id)
        .lt("id", current_scan_id)
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]

def get_findings_by_scan(scan_id):
    response = (
        supabase
        .table("findings")
        .select("*")
        .eq("scan_id", scan_id)
        .execute()
    )

    if not response.data:
        return []

    return response.data


def determine_current_state(current_finding, previous_findings):
    previous_finding = find_matching_finding(
        current_finding,
        previous_findings
    )

    status = "continued" if previous_finding is not None else "new"

    (
        supabase
        .table("findings")
        .update({"status": status})
        .eq("id", current_finding["id"])
        .execute()
    )

    return status

def find_resolved_findings(previous_findings, current_findings):
    resolved = []

    for previous_finding in previous_findings:
        current_match = find_matching_finding(
            previous_finding,
            current_findings
        )

        if current_match is None:
            (
                supabase
                .table("findings")
                .update({"status": "resolved"})
                .eq("id", previous_finding["id"])
                .execute()
            )
            resolved.append(previous_finding)

    return resolved