from pydantic import BaseModel
from datetime import datetime

class CreateAsset(BaseModel):
    host : str 
    
class AssetResponse(BaseModel):
    id : int
    user_id : int
    host : str 
    created_at : datetime
    
