from datetime import datetime
from src.schemas import GPSDataResponse
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


async def is_valid_datetime(date_str: str) -> bool:
    """
    Асинхронная функция для проверки корректности формата строки времени.

    :param date_str: Строка, представляющая дату и время.
    :type date_str: str
    :return: True, если строка представляет корректную дату и время, иначе False.
    :rtype: bool
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


async def fetch_last_geometry(session: AsyncSession) -> List[GPSDataResponse]:
    query = text(
        "SELECT DISTINCT ON (vehicle_id) vehicle_id, ST_AsText(location) AS geom "
        'FROM "GPS"'
        "ORDER BY vehicle_id, gps_time DESC;"
    )
    result = await session.execute(query)
    rows = result.all()

    gps_data_list = []
    for row in rows:
        gps_data_list.append(GPSDataResponse(vehicle_id=row.vehicle_id, location=row.geom))
    return gps_data_list


async def fetch_vehicle_last_geometry(vehicle_id: int, session: AsyncSession) -> GPSDataResponse:
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
        raise HTTPException(status_code=404, detail="Vehicle not found")


async def fetch_vehicle_track(vehicle_id: int,
                              start_datetime: str,
                              end_datetime: str,
                              session: AsyncSession) -> List[str]:
    if not (is_valid_datetime(start_datetime) and is_valid_datetime(end_datetime)):
        raise HTTPException(status_code=400, detail="Invalid start_datetime or end_datetime ('%Y-%m-%d %H:%M:%S')")

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
