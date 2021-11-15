import json
from fastapi import FastAPI, Response, Form, Depends
from sqlalchemy import select
from sqlmodel import Session

from .db import get_session, init_db
from .models import Weather, WeatherCreate
from .data import get_data_from_weather_api, post_request_sender


app = FastAPI()


@app.on_event("startup")
def on_startup():
    """Создаёт таблицу в базе данных при запуске приложения"""
    init_db()


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
def get_songs(session: Session = Depends(get_session)):
    """Получить данные из БД"""
    result = session.execute(select(Weather))
    requests = result.scalars().all()
    return [Weather(
        source=req.source,
        city=req.city,
        temp=req.temp,
        timezone=req.timezone,
        lon=req.lon,
        lat=req.lat,
        request=req.request,
        id=req.id)
            for req in requests]


@app.post("/db")
def add_request(req: WeatherCreate, session: Session = Depends(get_session)):
    """Добавляет запрос в базу данных"""
    req = Weather(
            source=req.source,
            city=req.city,
            temp=req.temp,
            timezone=req.timezone,
            lon=req.lon,
            lat=req.lat,
            request=req.request)
    session.add(req)
    session.commit()
    session.refresh(req)
    return req
