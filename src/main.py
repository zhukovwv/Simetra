from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from functions import fetch_last_geometry, fetch_vehicle_last_geometry, fetch_vehicle_track
from services import load_data_from_excel

app = FastAPI(
    title="GPS Service"
)


@app.get('/vehicles/')
async def get_vehicles_last_geometry(session: AsyncSession = Depends(get_async_session)):
    """
    Обработчик для получения последнего местоположения всех транспортных средств.

    :param session: Асинхронная сессия базы данных.
    :type session: sqlalchemy.ext.asyncio.AsyncSession
    :return: Список объектов местоположений транспортных средств.
    :rtype: list
    """
    return await fetch_last_geometry(session)


@app.get('/vehicles/{vehicle_id}')
async def get_vehicle_last_geometry(vehicle_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Обработчик для получения последнего местоположения конкретного транспортного средства.

    :param vehicle_id: Идентификатор транспортного средства.
    :type vehicle_id: int
    :param session: Асинхронная сессия базы данных.
    :type session: sqlalchemy.ext.asyncio.AsyncSession
    :return: Объект местоположения транспортного средства.
    :rtype: object
    """
    return await fetch_vehicle_last_geometry(vehicle_id, session)


@app.get('/vehicles/{vehicle_id}/track/{start_datetime}/{end_datetime}')
async def get_vehicle_track(vehicle_id: int,
                            start_datetime: str,
                            end_datetime: str,
                            session: AsyncSession = Depends(get_async_session)):
    """
    Обработчик для получения трека движения конкретного транспортного средства за определенный период времени.

    :param vehicle_id: Идентификатор транспортного средства.
    :type vehicle_id: int
    :param start_datetime: Начальная дата и время в формате '%Y-%m-%d %H:%M:%S'.
    :type start_datetime: str
    :param end_datetime: Конечная дата и время в формате '%Y-%m-%d %H:%M:%S'.
    :type end_datetime: str
    :param session: Асинхронная сессия базы данных.
    :type session: sqlalchemy.ext.asyncio.AsyncSession
    :return: Список координат транспортного средства за указанный период времени.
    :rtype: list
    """
    return await fetch_vehicle_track(vehicle_id, start_datetime, end_datetime, session)


# Только для теста!
@app.get('/load/gpsdata')
async def load_test_data():
    """
    Одно нажатие и тестовые gps данные будут в PostGis
    """
    file_path = "data/2_5420464171701519891.xlsx"
    await load_data_from_excel(file_path)
    return "GPS data loaded successfully!"
