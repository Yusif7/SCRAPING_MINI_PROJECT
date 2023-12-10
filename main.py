from functions import *
import time

# Testing site url
URL = 'https://programmer100.pythonanywhere.com/tours/'

if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        # Add like file

        if extracted != "No upcoming tours":  # If tour is exist
            row = read(extracted)
            if not row:  # If tour is not on data.txt file
                store(extracted)  # Add tour to data.txt file
                send_email()
        time.sleep(2)

