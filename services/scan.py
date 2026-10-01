from database import supabase

def create_scan(asset_id, tool):
    response = (
        supabase
        .table("scans")
        .insert({
            "asset_id": asset_id,
            "tool": tool
        })
        .execute()
    )

    return response.data[0]
