import os
from app.utils.utils import datetime_today
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
from prompt import prompt_message , prompt
from models import NewsResponse  
from datetime import datetime , timezone , timedelta
from typing import List
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

tools = [retrieve_context]
agent = create_agent(model , tools , system_prompt=prompt)


def rssfeeds_to_text(urls):
    """ for a list of rss links scrape all the text with source and media url """
    articles_url_list = []
    for url in urls :
        url_list = list_generator(url)
        articles_url_list += url_list

    print("Generated List of all article links from all rss feeds ")
    extracted_text = all_articles_text(articles_url_list)
    print("Final Text to be passed into the LLM extraced ")
    return extracted_text



def list_generator(feed_url):
    """ get article links from rss feed link """
    list = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries :
        media_link=" "
        if 'media_content' in entry:
            media_link = entry.media_content[0]["url"]
        elif 'href' in entry["links"][1]:
            media_link =  entry["links"][1]['href']

        item = {"url":entry.link , "media_link": media_link}
        list.append(item)
    return list


def all_articles_text(items_list):
    final_text = " "
    for item in items_list:
        url = item["url"]
        text = article_scrape(url).text
        media_link = item["media_link"]
        final_text += f"article_text:{text} url:{url} image_url:{media_link} "
    return final_text

def article_scrape(url):
    article = Article(url)
    article.download()
    article.parse()
    return article 



def link_to_doc(url):
    article = article_scrape(url)
    doc= Document(page_content= article.text , metadata={"source":url})
    return doc



def final_document(url_list):
    """ Scrape the text from the urls in the list and return  list of Document() """
    final_document = []
    for url in url_list:
        doc = link_to_doc(url)
        final_document.append(doc)
    return final_document

def get_news_data():
    start = datetime_today()
    end = start + timedelta(days=1)
    data = collection.find_one(
    {"date": {"$gte": start, "$lt": end}},
    {"_id": 0}
)
    return data


# Daily brief generation by passing rss_feed list 
def day_brief_generator(rssfeed_list : List[str] ):
    final_text = rssfeeds_to_text(rssfeed_list)
    print("final text passed into the LLM ")

    system_message = SystemMessage(prompt_message)
    human_message = HumanMessage(final_text)
    conversation = [system_message , human_message ]

    model_with_structure = model.with_structured_output(NewsResponse)
    response = model_with_structure.invoke(conversation)
    print("Response Recieved from the LLM")
    if len(response.news_items) > 24:
        print ("Items more than 25 reducing")
        response.news_items = response.news_items[:24]
        response.urls = response.urls[:24]

    #response = model.invoke(conversation)
    #print(response.content)

    # Inserting into db
    today = datetime_today()
    updated_response = response.model_copy(update={"date": today })
    collection.insert_one(updated_response.model_dump())
    print("Successfully inserted into DB ")

# Embedding selected articles into DB 
def embeddings_to_vector_store():
    data = get_news_data()
    url_list = data["urls"]

    document = final_document(url_list)
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(document)
    collection_em.delete_many({})
    vector_store.create_vector_search_index(dimensions=3072)
    vector_store.add_documents(documents=all_splits)
    print("successfully embedded text")


# Main function to do add Briefing and Embedding to the backend
def generate_brief_insert_embedding():
    rssfeed_list= ["https://feeds.feedburner.com/ndtvnews-top-stories"   ,"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms" , "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms" , "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"  ]
    day_brief_generator(rssfeed_list)
    print("Done with Generating Daily Briefing")
    embeddings_to_vector_store()
    print("Embedding done to the vector store ")


# To query the Vector Store to recieve Relevant response 
def run_query(query:str):
    user_message = HumanMessage(query)
    messages = [user_message]
    response = agent.invoke({"messages":messages})
    return response

