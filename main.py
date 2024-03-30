from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

app = FastAPI(
    title="GPS Service"
)


class GPSDataResponse(BaseModel):
    vehicle_id: int
    location: str


async def is_valid_datetime(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


@app.get('/vehicles/')
async def vehicles_last_geometry(session: AsyncSession = Depends(get_async_session)):
    query = text(
        "SELECT DISTINCT ON (vehicle_id) vehicle_id, ST_AsText(location) AS geom "
        'FROM "GPS"'
        "ORDER BY vehicle_id, gps_time DESC;"
    )
    result = await session.execute(query)
    rows = result.all()

    # Преобразуем результаты запроса в список объектов GPSDataResponse
    gps_data_list = []
    for row in rows:
        gps_data_list.append(GPSDataResponse(vehicle_id=row.vehicle_id, location=row.geom))
    return gps_data_list


@app.get('/vehicles/{vehicle_id}')
async def vehicle_last_geometry(vehicle_id: int, session: AsyncSession = Depends(get_async_session)):
    query = text(
        "SELECT vehicle_id, ST_AsText(location) AS geom "
        'FROM "GPS" '
        'WHERE vehicle_id = :vehicle_id '
        'ORDER BY gps_time DESC '
        'LIMIT 1;'
    )
    result = await session.execute(query, {"vehicle_id": vehicle_id})
    row = result.first()
    if row:
        return GPSDataResponse(vehicle_id=row.vehicle_id, location=row.geom)
    else:
        return None


@app.get('/vehicles/{vehicle_id}/track/{start_datetime}/{end_datetime}')
async def vehicle_track(vehicle_id: int,
                        start_datetime: str,
                        end_datetime: str,
                        session: AsyncSession = Depends(get_async_session)):
    if is_valid_datetime(start_datetime) and is_valid_datetime(end_datetime):
        raise HTTPException(status_code=400, detail="Not valid start_datetime or end_datetime ('%Y-%m-%d %H:%M:%S')")

    if start_datetime >= end_datetime:
        raise HTTPException(status_code=400, detail="The start date and time must be less than the end date.")

    query = text(
        "SELECT ST_AsText(location) AS geom "
        'FROM "GPS" '
        "WHERE vehicle_id = :vehicle_id "
        "AND gps_time >= :start_datetime "
        "AND gps_time <= :end_datetime "
        "ORDER BY gps_time;"
    )
    result = await session.execute(query, {"vehicle_id": vehicle_id,
                                           "start_datetime": start_datetime,
                                           "end_datetime": end_datetime})
    rows = result.all()

    gps_data_list = []
    for row in rows:
        gps_data_list.append(row.geom)
    return gps_data_list
