from pydantic import BaseModel


class ItemsDeleted(BaseModel):
    result_text: str
