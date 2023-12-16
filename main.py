from functions import *
import time

# Testing site url
URL = 'https://programmer100.pythonanywhere.com/tours/'

if __name__ == '__main__':
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)

        # Add like file

        if extracted != "No upcoming tours":  # If tour is exist
            database = Database()
            row = database.read(extracted)
            print(extracted)
            if not row:  # If tour is not on data.txt file
                database.store(extracted)  # Add tour to data.txt file
                email = Email()
                email.send()
        time.sleep(2)

