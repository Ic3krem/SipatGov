from pydantic import BaseModel


class LGUListItem(BaseModel):
    id: int
    name: str
    lgu_type: str
    transparency_score: float | None = None
    latitude: float | None = None
    longitude: float | None = None

    model_config = {"from_attributes": True}


class LGUMapMarker(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    score: float
    type: str

    model_config = {"from_attributes": True}
