from pydantic import BaseModel , Field
from datetime import datetime

class CreateScan(BaseModel):
    tool : str = Field(min_length=3,max_length=10)
    
class ScanResponse(BaseModel):
    id : int
    asset_id : int
    tool : str
    created_at : datetime
    
    