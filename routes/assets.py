from fastapi import APIRouter, Depends

from database import supabase
from schemas.asset import CreateAsset, AssetResponse
from utils.auth import get_current_user

router = APIRouter()


@router.post("/assets", response_model=AssetResponse)
def create_asset(
    asset: CreateAsset,
    current_user: dict = Depends(get_current_user)
):
    new_asset = {
        "user_id": current_user["id"],
        "host": asset.host
    }

    response = supabase.table("assets").insert(new_asset).execute()

    return response.data[0]