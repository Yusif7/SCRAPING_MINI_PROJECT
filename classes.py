import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    # Function for scraping datat from site
    def scrape(self, url):
        # Scrape the data from site
        response = requests.get(url, headers=HEADERS)
        # Convert url format to text
        source = response.text
        return source

    # Function for extracting needed block code from html file
    def extract(self, source):
        # Create yaml file for describing which id or class we need
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        # Convert content of yaml file to dictionary type and extract the value of tours key
        value = extractor.extract(source)["tours"]
        return value


class Database:
    # Method which see both methods below the class and self give access to all method inside the class
    # Method init automatically execute when we create instance of class, other methods inside the execute only if we call instance of method
    def __init__(self):
        # Create connection between database and project
        self.connection = sqlite3.connect('data.db')

    # Function for store our data
    def store(self, extracted):
        # 'a' not overwriting data to file , it is only append new data
        # with open('data.txt', 'a') as file:
        # file.write(extracted + '\n')
        row = extracted.split(',')
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        # Add/save data in our database
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        # Save changes
        self.connection.commit()

    # Function help us to use content of this file in the if condition below
    def read(self, extracted):
        # Convert string to list
        row = extracted.split(',')
        # For loop need for extracting row without useless spaces
        row = [item.strip() for item in row]
        # Equal database columns to on value and use which you need
        band, city, date = row
        # Syntax for using multi row value in python
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        return rows


class Email:
    # Function sends us an email every time when it found new tour
    def send(self):
        host = "smtp.gmail.com"
        port = 465
        username = 'learningtestemail7@gmail.com'
        password = os.getenv('TEST_PASSWORD')
        receiver = 'learningtestemail7@gmail.com'
        context = ssl.create_default_context()
        message = """\
    Subject: Notification about new tour is coming...
    
    Tour name ........
    """
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
        print('Email sent successfully!')
