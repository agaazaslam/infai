from fastapi.responses import JSONResponse
from news import generate_brief_insert_embedding, run_query
from fastapi import FastAPI, HTTPException, status
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

@app.get('/')
def home():
    return {"message":"Main route for the InfAI backend "}



@app.get('/health')
def health():
    return {"message":"Everything working fine "}

@app.get('/news-today')
def get_news():
    response =  get_news_data()
    if response is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND , content={"message" : "No data found for today "})
    return response


@app.post('/query' , response_model = QueryResponse )
def query_request(request:QueryRequest):
    response = run_query(request.message) 
    final_msg = response["messages"][-1].content
    time = formatted_time()

    return {"message" : final_msg , "role":"assistant" , "time": time }


@app.get('/briefing-embedding-generation')
def gen_brief_embed():
    try:
        generate_brief_insert_embedding()
        data = {"message" : "Everything Generated Successfully"}
        return JSONResponse(status_code=202 , content=data)


    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f" Interval Error : {str(e)} ") 
