from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[str]
    title: str
    authors: str
    isbn: Optional[str]
    publisher: str
    language: str
    number_of_pages: int
    release: str
    image_url: str