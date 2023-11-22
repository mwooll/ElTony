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
    hasGender: bool
    Pr_Male: Optional[float]
    Egg_Group_1: str
    Egg_Group_2: Optional[str]
    hasMegaEvolution: bool
    Height_m: float
    Weight_kg: float
    Catch_Rate: int
    Body_Style: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

