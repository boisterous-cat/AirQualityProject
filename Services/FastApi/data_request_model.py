from pydantic import BaseModel, Field, NonNegativeFloat
from typing import Optional
from typing import List


class MlRequest(BaseModel):
    co: Optional[float] = Field(0, ge=0, le=1000)
    no: Optional[float] = Field(0, ge=0, le=1000)
    ozone: Optional[float] = Field(0, ge=0, le=1000)
    pm2: Optional[float] = Field(0, ge=0, le=1000)


class MlRequests(BaseModel):
    objects: List[MlRequest]


class UserLocation(BaseModel):
    Country: str
    City: str