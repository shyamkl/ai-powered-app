from pydantic import BaseModel

class Location(BaseModel):

    lat: float

    lon: float


class Venue(BaseModel):
    id:int
    name:str
    lat:float
    lon:float
    address:str
    city:str
    category:str