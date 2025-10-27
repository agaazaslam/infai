from datetime import datetime

# Get current time
def formatted_time():
    """ Get Time in 11:45 PM like format """
    now = datetime.now()
    # Format as hh:mm AM/PM
    time_str = now.strftime("%I:%M %p") 
    return time_str
