from datetime import datetime , timezone , date


now = datetime.now(timezone.utc).isoformat()
date = date.today()
print(now)
print(date)
