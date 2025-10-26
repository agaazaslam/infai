from datetime import datetime , timedelta 
from ..config.db import collection


def get_news_data():
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    print(start)
    end = start + timedelta(days=1)
    data = collection.find_one(
    {"date": {"$gte": start, "$lt": end}},
    {"_id": 0}
)
    return data


