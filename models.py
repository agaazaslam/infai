from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query : str 

class QueryResponse(BaseModel):
    content: str


class NewsItem(BaseModel):
    headline: str
    summary: str
    url : str = Field (... , description="The url of the article ")

class Category(BaseModel):
    category: str
    items: List[NewsItem]

class NewsResponse(BaseModel):
    date : datetime = Field(... , description="today's date and time  ")
    articles: int = Field(... , description="total number of articles in the response ")
    categories: List[Category]
    tokens_consumed : int = Field(... , description="total token used combining input and output give the correct value")
    urls : List[str] = Field (... , description= " all the urls ")


