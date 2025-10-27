from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    time : str
    message : str 
    role: str

class QueryResponse(BaseModel):
    time : str
    message: str
    role: str


class NewsItem(BaseModel):
    headline: str
    summary: str
    category : str = Field(... , description="category the news item comes under ")
    tags : List[str] = Field(... , description="types we can give the news article")
    url : str = Field (... , description="The url of the article ")
    image_url : str = Field (... , description="The image url of the article ")


class NewsResponse(BaseModel):
    date : datetime = Field(... , description="today's date and time")
    articles: int = Field(... , description="total number of articles in the response ")
    news_items : List[NewsItem]
    category : List[str]= Field(... , description=" Categories of news article present in response ")
    urls : List[str] = Field (... , description= " all the urls ")


