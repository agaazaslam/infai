import { LoaderCircle, SearchX } from "lucide-react"
import Footer from "../components/Footer"
import NewsCard from "../components/NewsCard";
import { useEffect, useState } from "react";
import type { NewsItem } from "../types/news";
import axios from "axios";
import Header from "../components/Header";

const dummy = {
  "headline": "Albania Appoints AI Minister Pregnant with 83 \"Children\" to Assist Parliament",
  "summary": "Albania's Prime Minister announced the appointment of \"Diella,\" an AI minister, who is \"pregnant\" with 83 assistants to aid parliament members.",
  "category": "International",
  "tags": [
    "AI",
    "Government",
    "Technology"
  ],
  "url": "https://www.ndtv.com/world-news/diella-ai-minister-pregnant-with-83-children-albania-pms-bizarre-announcement-9519522",
  "image_url": "https://c.ndtvimg.com/2025-10/rdihfi1g_albania-ai-minister-_625x300_26_October_25.jpg?im=FitAndFill,algorithm=dnn,width=1200,height=738"
}



const News = () => {
  const date = new Date();

  const baseUrl = "http://localhost:8000";

  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);

  const fetchNews = async () => {
    setLoading(true)
    try {

      const response = await axios.get(`${baseUrl}/news-today`);
      const data = response.data;
      const newsItems = data.news_items;
      console.log(newsItems);
      setNews(newsItems);


    }

    catch (currentError) {

      setError(true);
      console.log(currentError);

    }
    finally {

      setLoading(false)
    }

  }

  useEffect(() => { fetchNews(); }, [])


  return (
    <div className="min-h-screen flex flex-col w-full text-neutral-content">

      <Header />


      <div className=" flex flex-col grow p-4">

        <h1 className="text-xl text-neutral font-semibold"> Latest News: {date.toLocaleDateString()} </h1>
        <div className="mx-auto w-full my-8  md:max-w-5xl  lg:max-w-7xl  flex flex-wrap grow gap-10 justify-center items-center  bg-base-200 rounded-2xl border-1 p-5 pt-10 ">

          {isLoading && <div> <LoaderCircle className="animate-spin w-24 h-24 text-neutral " />   </div>}

          {!isLoading && error && (<div className="flex flex-col justify-center items-center"> <SearchX className="w-24 h-24 text-neutral" /> Could not find today's Data </div>)}

          {!isLoading && news && (<>
            {news.map((newsItem: NewsItem) => <NewsCard key={newsItem.url} data={newsItem} />)}

          </>)}


        </div>



      </div>


      <Footer />

    </div>
  )
}

export default News

