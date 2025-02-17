from pydantic import BaseModel, Field
from typing import Literal

class Coordinates(BaseModel):
    x: int = Field(..., description="The x (pixels from the left edge)")
    y: int = Field(..., description="y (pixels from the top edge)")

class ClickAction(BaseModel):
    x: int = Field(..., description="X coordinate on the page")
    y: int = Field(..., description="Y coordinate on the page")

class TypeAction(BaseModel):
    text: str = Field(..., description="Text to type")
    
class WaitTime(BaseModel):
    time: int = Field(..., description="Time to wait in seconds")