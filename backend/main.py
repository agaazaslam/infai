from news import run_query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse 
from app.services.news_service import get_news_data
from app.utils.utils import formatted_time
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

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
    response = run_query(request.message) 
    final_msg = response["messages"][-1].content
    time = formatted_time()

    return {"message" : final_msg , "role":"assistant" , "time": time }


