from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from database import supabase

from parsers.nmap import parse_nmap
from parsers.zap import parse_zap

from services.normalize import (
    normalize_nmap_findings,
    normalize_zap_findings
)

from services.scan import create_scan
from services.scoring import calculate_raw_score

from services.delta import (
    get_previous_scan,
    get_findings_by_scan,
    determine_current_state,
    find_resolved_findings
)

from utils.auth import get_current_user


router = APIRouter()


@router.post("/scan/{asset_id}")
def upload_scan(
    asset_id: int,
    tool: str,
    current_user: dict = Depends(get_current_user)
):
    asset_response = (
        supabase.table("assets")
        .select("*")
        .eq("id", asset_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not asset_response.data:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    response = create_scan(asset_id, tool)

    return response


@router.post("/scan/{asset_id}/upload")
def upload_nmap_scan(
    asset_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    asset_response = (
        supabase.table("assets")
        .select("*")
        .eq("id", asset_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not asset_response.data:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    scan = create_scan(asset_id, "nmap")

    previous_scan = get_previous_scan(
        asset_id,
        scan["id"]
    )

    previous_findings = []

    if previous_scan:
        previous_findings = get_findings_by_scan(
            previous_scan["id"]
        )

    parsed_results = parse_nmap(file.file)

    findings = normalize_nmap_findings(parsed_results)

    saved_findings = []

    for finding in findings:
        finding_data = {
        "scan_id": scan["id"],
        "title": finding["title"],
        "description": finding["description"],
        "severity": finding["severity"],
        "cve_id": finding["cve_id"],
        "host": finding["host"],
        "port": finding["port"],
        "endpoint": finding["endpoint"],
        "cvss_score": calculate_raw_score(finding["severity"])
    }

        response = (
            supabase
            .table("findings")
            .insert(finding_data)
            .execute()
        )

        saved_findings.append(response.data[0])

    for finding in saved_findings:
        determine_current_state(
            finding,
            previous_findings
        )

    current_findings = get_findings_by_scan(scan["id"])

    if previous_findings:
        find_resolved_findings(
            previous_findings,
            current_findings
        )

    return {
        "scan": scan,
        "findings": get_findings_by_scan(scan["id"])
    }


@router.post("/scan/{asset_id}/upload-zap")
def upload_zap_scan(
    asset_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    asset_response = (
        supabase.table("assets")
        .select("*")
        .eq("id", asset_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not asset_response.data:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    scan = create_scan(asset_id, "zap")

    previous_scan = get_previous_scan(
        asset_id,
        scan["id"]
    )

    previous_findings = []

    if previous_scan:
        previous_findings = get_findings_by_scan(
            previous_scan["id"]
        )

    parsed_results = parse_zap(file.file)

    findings = normalize_zap_findings(parsed_results)

    saved_findings = []

    for finding in findings:
        finding_data = {
        "scan_id": scan["id"],
        "title": finding["title"],
        "description": finding["description"],
        "severity": finding["severity"],
        "cve_id": finding["cve_id"],
        "host": finding["host"],
        "port": finding["port"],
        "endpoint": finding["endpoint"],
        "cvss_score": calculate_raw_score(finding["severity"])
    }

        response = (
            supabase
            .table("findings")
            .insert(finding_data)
            .execute()
        )

        saved_findings.append(response.data[0])

    for finding in saved_findings:
        determine_current_state(
            finding,
            previous_findings
        )

    current_findings = get_findings_by_scan(scan["id"])

    if previous_findings:
        find_resolved_findings(
            previous_findings,
            current_findings
        )

    return {
        "scan": scan,
        "findings": get_findings_by_scan(scan["id"])
    }

