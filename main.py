from pydantic import BaseModel
from llm import run_query 
from fastapi import FastAPI
from fastapi.responses import StreamingResponse 
app = FastAPI()

class QueryRequest(BaseModel):
    query : str 

@app.get('/health')
def health():
    return {"message":"Everything working fine "}

@app.get('/')
def home():
    return {"message":"Main route for the InfAI backend "}

@app.post('/query')
def query(request :QueryRequest):
    def event_generator():
        for chunk in run_query(request.query):
            yield f"data: {chunk} \n\n"

    return StreamingResponse(event_generator(), media_type = "text/event-stream")

