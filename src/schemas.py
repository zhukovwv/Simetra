from pydantic import BaseModel


class GPSDataResponse(BaseModel):
    """
    Модель данных для ответа на запрос, содержащая информацию о местоположении транспортного средства.
    """
    vehicle_id: int
    location: str
