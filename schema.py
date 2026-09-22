from pydantic import BaseModel, Field

class URL(BaseModel):
    url: str = Field(min_length=10, max_length=256)