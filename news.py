from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from langchain_core.documents import Document
from newspaper import Article 


load_dotenv()

loader = WebBaseLoader("");

url = " https://www.ndtv.com/india-news/sale-of-air-purifiers-rises-in-delhi-as-air-quality-remains-in-poor-category-9511322#publisher=newsstand" 
url2 = "https://timesofindia.indiatimes.com/india/police-political-pressure-satara-woman-doctors-suicide-gets-murky-kin-makes-big-claim-cop-suspended/articleshow/124783512.cms"
url3 = "https://www.indiatoday.in/elections/story/would-choose-death-over-returning-to-rjd-not-hungry-for-power-tej-pratap-yadav-2808027-2025-10-24?utm_source=rss"
url5 = "https://www.news18.com/india/fire-breaks-out-in-amritsar-purnia-jan-sewa-express-near-sonbarsha-9657023.html"

url_list = [ url , url2 , url3 , url5 ]

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
        text = doc.page_content
        final_text = final_text + text 
    return final_text
    

final_text = all_articles_text(url_list)
print(final_text)



model = init_chat_model("google_genai:gemini-2.5-flash-lite")

    
