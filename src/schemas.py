from pydantic import BaseModel


class GPSDataResponse(BaseModel):
    vehicle_id: int
    location: str
