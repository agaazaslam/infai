from news import run_query
from fastapi import FastAPI
from models import QueryRequest, QueryResponse 
from app.services.news_service import get_news_data
app = FastAPI()

@app.get('/health')
def health():
    return {"message":"Everything working fine "}

@app.get('/')
def home():
    return {"message":"Main route for the InfAI backend "}

@app.get('/news-today')
def get_news():
    response =  get_news_data()
    return response


@app.post('/query' , response_model = QueryResponse )
def query_request(request:QueryRequest):
    response = run_query(request.query) 
    final_msg = response["messages"][-1].content

    return {"content" : final_msg }

