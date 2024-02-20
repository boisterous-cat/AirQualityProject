from pydantic import BaseModel, validator, root_validator
from typing import Optional


class MlRequest(BaseModel):
    co: float
    no: float
    ozone: float
    pm2: float