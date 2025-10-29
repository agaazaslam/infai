from datetime import datetime 
from zoneinfo import ZoneInfo


# Get current time
def formatted_time():
    """ Get Time in 11:45 PM like format """
    now = datetime.now()
    # Format as hh:mm AM/PM
    time_str = now.strftime("%I:%M %p") 
    return time_str

def datetime_today():
    return datetime.now(ZoneInfo("UTC")).replace(hour=0, minute=0, second=0, microsecond=0)


