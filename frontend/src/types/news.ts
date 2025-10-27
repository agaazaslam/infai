


export interface NewsResponse {
  date: string; // today's date and time (ISO string from Python datetime)
  articles: number; // total number of articles in the response
  news_items: NewsItem[];
  category: string[]; // Categories of news articles present in response
  urls: string[]; // all the URLs
}






export interface NewsItem {
  headline: string;
  summary: string;
  category: string; // category the news item comes under
  tags: string[]; // types we can give the news article
  url: string; // The URL of the article
  image_url: string; // The image URL of the article
}


