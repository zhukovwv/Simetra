from fastapi import FastAPI

app = FastAPI(
    title="GPS Service"
)


@app.get('/vehicles/')
async def vehicles_last_geometry():
    return 'Hello'


@app.get('/vehicles/{vehicle_id}')
def vehicle_last_geometry(vehicle_id: int):
    return 'Hello'


@app.get('/vehicles/{vehicle_id}/track')
def vehicle_track(vehicle_id: int):
    return 'Hello'