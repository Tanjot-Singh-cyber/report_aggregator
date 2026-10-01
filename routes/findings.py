from fastapi import APIRouter, Depends, HTTPException

from database import supabase
from utils.auth import get_current_user

router = APIRouter()


@router.get("/scans/{scan_id}/findings")
def get_scan_findings(
    scan_id: int,
    current_user: dict = Depends(get_current_user)
):
    scan_response = (
        supabase.table("scans")
        .select("id, asset_id")
        .eq("id", scan_id)
        .execute()
    )

    if not scan_response.data:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    scan = scan_response.data[0]

    asset_response = (
        supabase.table("assets")
        .select("id")
        .eq("id", scan["asset_id"])
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not asset_response.data:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    findings_response = (
        supabase.table("findings")
        .select("*")
        .eq("scan_id", scan_id)
        .execute()
    )

    return findings_response.data