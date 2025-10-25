import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from newspaper import Article
import feedparser
from pymongo import MongoClient
from prompt import prompt_message
from models import NewsResponse  


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["infai"]
collection_em=db["articles-embedding"]
collection = db["news-summary"]

model = init_chat_model("google_genai:gemini-2.5-flash-lite")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001" )
vector_store = MongoDBAtlasVectorSearch(collection=collection_em , embedding=embeddings , index_name="news-summary-index" , relevance_score_fn="cosine")


@tool(response_format="content_and_artifact")
def retrieve_context(query:str ):
    """" Retrieve information to help answer query """
    retrieved_documents = vector_store.similarity_search(query , k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_documents
    )
    return serialized , retrieved_documents


prompt = """
You are a summarization agent. You can access a tool called 'retrieve_context' to fetch
relevant passages from news articles. After retrieval, always summarize the context and
provide a concise, human-readable answer. Act as a news analyst and give to the point and detail
oriented answers
"""

tools = [retrieve_context]

agent = create_agent(model , tools , system_prompt=prompt)


def list_generator(feed_url):
    list = []
    feed = feedparser.parse(feed_url)
    print(len(feed.entries))
    for entry in feed.entries :
        list.append(entry.link)
    return list


def article_scrape(url):
    article = Article(url)
    article.download()
    article.parse()
    return article 



def document_maker(url):
    article = article_scrape(url)
    doc= Document(page_content= article.text , metadata={"source":url})
    return doc

def all_articles_text(url_list):
    final_text = ""
    for url in url_list:
        doc = document_maker(url)
        text = doc.page_content.strip()
        url = doc.metadata["source"]
        final_text = final_text + text + " " + url + " "
    return final_text



def documents_maker(url_list):
    final_document = []
    for url in url_list:
        doc = document_maker(url)
        final_document.append(doc)
    return final_document

def get_news_data(date_prefix):
    data = collection.find_one({"date": {"$regex": f"^{date_prefix}"}} , {"_id":0})
    return data



def embeddings_to_vector_store(url_list):
    document = documents_maker(url_list)
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(document)
    vector_store.create_vector_search_index(dimensions=3072)
    vector_store.add_documents(documents=all_splits)
    print("successfully embedded text")

# Filtering & Summarizing Top 25 Articles 
def summarize(url_list):
    final_text = all_articles_text(url_list)

    system_message = SystemMessage(prompt_message)
    human_message = HumanMessage(final_text)
    conversation = [system_message , human_message ]

    model_with_structure = model.with_structured_output(NewsResponse)
    response = model_with_structure.invoke(conversation)

    #response = model.invoke(conversation)
    #print(response.content)
    #print(response.usage_metadata)

    print(response)
    collection.insert_one(response.model_dump())
    return response



def run_query(query:str):
    user_message = HumanMessage(query)
    messages = [user_message]
    response = agent.invoke({"messages":messages})
    return response







# Testing all the functions

#summarize(url_list)
#list_1 = list_generator("https://feeds.feedburner.com/ndtvnews-top-stories")
#list_2 = list_generator("https://feeds.feedburner.com/ndtvnews-world-news")
#list_4 = list_generator("https://www.indiatoday.in/rss/home")
#combined_list = list_1 + list_2 + list_4

#response = summarize(combined_list)
#collection.insert_one(response.model_dump())


#response = summarize(list_1)
#updated_response = response.model_copy(update={"date": datetime.now(timezone.utc).isoformat() })
#collection.insert_one(updated_response.model_dump())

#date_prefix = "2025-10-25"
#messages = collection.find_one({"date": {"$regex": f"^{date_prefix}"}})

#print(messages["urls"])

#embeddings_to_vector_store(messages["urls"])



