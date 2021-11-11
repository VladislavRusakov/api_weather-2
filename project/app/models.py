from sqlmodel import SQLModel, Field


class WeatherBase(SQLModel):
    source: str
    city: str
    temp: str
    timezone: str
    lon: str
    lat: str
    request: str


class Weather(WeatherBase, table=True):
    id: int = Field(default=None, primary_key=True)


class WeatherCreate(WeatherBase):
    pass
