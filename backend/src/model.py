from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from typing import Optional
from pydantic import BaseModel
from typing import Union


class Pokemon(BaseModel):
    Number: int
    Name: str
    Type_1: str
    Type_2: Union[str, None]
    TypeColor: Optional[str]
    Total: int
    HP: int
    Attack: int
    Defense: int
    Sp_Atk: int
    Sp_Def: int
    Speed: int
    Generation: int
    isLegendary: bool
    Color: str
    Body_Style: str
    image: str
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

