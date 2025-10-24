import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool
from langchain_core.messages.utils import _chunk_to_msg
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_google_genai  import GoogleGenerativeAIEmbeddings
from pymongo import MongoClient
from langchain.agents import create_agent
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessageChunk, HumanMessage
import json
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["vector-embeddings"]
collection = db["animal-farm"]


file_path = "animal-farm.pdf"
#loader = PyPDFLoader(file_path)

#docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
#all_splits = text_splitter.split_documents(docs)
#print(len(all_splits))

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001" )

vector_store = MongoDBAtlasVectorSearch(collection=collection , embedding=embeddings , index_name="animal-farm-index" , relevance_score_fn="cosine")

#vector_store.create_vector_search_index(dimensions=3072)

#vector_store.add_documents(documents=all_splits[15:])




#ids = vector_store.add_documents(documents=all_splits[10:])

#results = vector_store.similarity_search("Who led the animals after the rebellion" , k=2)

#for res in results:
#    print(f" * {res.page_content}")


#print(results[0])



model = init_chat_model("google_genai:gemini-2.0-flash-lite")

@tool(response_format="content_and_artifact")
def retrieve_context(query:str ):
    """" Retrieve information to help answer query """
    retrieved_documents = vector_store.similarity_search(query , k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_documents
    )
    return serialized , retrieved_documents



prompt = (
    "You have access to a tool that retrieves context from a pdf book. "
    "Use the tool to help answer user queries."
)

tools = [retrieve_context]

agent = create_agent(model , tools , system_prompt=prompt)


def run_query(query:str):
    messages = [] 
    for token , metadata in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="messages"):

        if token.type == "AIMessageChunk":
            if token.content != "":
                safe_chunk = json.dumps(token.content)
                yield safe_chunk
                messages.append(token.content)
    print("Full AI Message : " , "".join(messages))










