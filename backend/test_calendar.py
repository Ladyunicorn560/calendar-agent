from calendar_utils import authenticate_google, check_availability, book_meeting
import datetime

service = authenticate_google()
start = datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=5)
end = start + datetime.timedelta(minutes=30)

# Check availability
events = check_availability(service, start, end)
if events:
    print("Not available")
else:
    link = book_meeting(service, "Test Meeting", start, end)
    print("Meeting booked:", link)
