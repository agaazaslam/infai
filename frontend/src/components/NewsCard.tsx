import { ExternalLink } from "lucide-react"
import type React from "react";
import type { NewsItem } from "../types/news";


interface NewsCardProps {
  data: NewsItem

}



const NewsCard: React.FC<NewsCardProps> = ({ data }) => {
  return (
    <div className="card bg-base-100 w-96 card-sm md:card-md  lg:card-lg shadow-sm">
      <figure>
        <img
          src={data.image_url}
          alt="Shoes"
          className="object-cover" />
      </figure>
      <div className="card-body">
        <h2 className="card-title text-base-content">
          {data.headline}
        </h2>
        <p className="text-base-content/70">
          {data.summary}

        </p>
        <div className="card-actions justify-end">
          <a href={data.url} target="_blank" rel="noopener noreffer" className=""> <ExternalLink /></a>
        </div>
      </div>
    </div>
  )
}

export default NewsCard
