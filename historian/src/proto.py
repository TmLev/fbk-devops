from pydantic import BaseModel


class Entry(BaseModel):
    data: str
