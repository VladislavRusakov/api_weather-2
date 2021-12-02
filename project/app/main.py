import json
from fastapi import FastAPI, Response, Form, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .db import get_session, init_db
from .models import Weather, WeatherCreate
from .data import get_data_from_weather_api, post_request_sender


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    """Создаёт таблицу в базе данных при запуске приложения"""
    await init_db()


@app.get("/ping")
async def pong():
    """"""
    return {"ping": "pong!"}


@app.get("/")
def index_page():
    """Рендер главной страницы"""
    with open('app/templates/index.html', 'r') as f:
        index_page = f.read()
    return Response(index_page, media_type='text/html')


@app.post("/api")
def data_from_frontend_form(city: str = Form(...)):
    """Позволяет получить данные с помощью запроса из формы"""
    try:
        response = get_data_from_weather_api(city)
        print(response)
        post_request_sender(response)
        return Response(json.dumps(response), media_type='text/html')
    except KeyError:
        return Response("<h1>Incorrect city name</h1>", media_type='text/html')


@app.get("/api/{city}")
def api_response(city: str):
    """Позволяет получить данные с помощью API"""
    try:
        response = get_data_from_weather_api(city)
        print(response)
        post_request_sender(response)
        return Response(json.dumps(response), media_type='text/html')
    except KeyError:
        return Response("<h1>Incorrect city name</h1>", media_type='text/html')


@app.get("/db", response_model=list[Weather])
async def get_db(session: AsyncSession = Depends(get_session)):
    """Получить данные из БД"""
    result = await session.execute(select(Weather))
    requests = result.scalars().all()
    return [Weather(
        source=req.source,
        city=req.city,
        temp=req.temp,
        timezone=req.timezone,
        lon=req.lon,
        lat=req.lat,
        request=req.request,
        datetime=req.datetime,
        id=req.id)
            for req in requests]


@app.post("/db")
async def add_request(req: WeatherCreate,
                      session: AsyncSession = Depends(get_session)):
    """Добавляет запрос в базу данных"""
    req = Weather(
            source=req.source,
            city=req.city,
            temp=req.temp,
            timezone=req.timezone,
            lon=req.lon,
            lat=req.lat,
            request=req.request,
            datetime=req.datetime)
    session.add(req)
    await session.commit()
    session.refresh(req)
    return req


@app.get("/db/del/{index}", response_model=list[Weather])
async def delete_row(index: int,
                     session: AsyncSession = Depends(get_session)):
    """Позволяет удалять записи из БД по индексу"""
    try:
        row = await session.execute(select(
            Weather).where(Weather.id == index))
        row = row.scalar_one()

        if index % 2 == 0:
            sub_row = await session.execute(select(
                Weather).where(Weather.id == index - 1))
            sub_row = sub_row.scalar_one()
        else:
            sub_row = await session.execute(select(
                Weather).where(Weather.id == index + 1))
            sub_row = sub_row.scalar_one()

    except NoResultFound:
        return Response("<h1>Index not found</h1>", media_type='text/html')

    await session.delete(row)
    await session.delete(sub_row)
    await session.commit()

    return index_page()
