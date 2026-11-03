from datetime import datetime, timedelta

today = datetime.now()
weeks_52_later = today + timedelta(weeks=52)
print(weeks_52_later) 
