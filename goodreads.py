import requests
import xml.etree.ElementTree as ET
import time
import csv

class Book(object):
    headers = ["id", "isbn", "author", "title", "isbn13", "asin", "kindle_asin", "marketplace_id", "country_code", "publication_date", "publisher", "language_code", "is_ebook"]

    def __init__(self, elementTree):
        et = elementTree.find('book')

        self.id = et.find('id').text
        self.isbn = et.find('isbn').text
        self.author = ""
        self.title = et.find('title').text
        self.isbn13 = et.find("isbn13").text
        self.asin = et.find("asin").text
        self.kindle_asin = et.find("kindle_asin").text
        self.marketplace_id = et.find("marketplace_id").text
        self.country_code = et.find("country_code").text
        self.publication_date = et.find("publication_year").text + "/" + et.find("publication_month").text + "/" + et.find("publication_day").text
        self.publisher = et.find("publisher").text
        self.language_code = et.find("language_code").text
        self.is_ebook = et.find("is_ebook").text
 
    def __repr__(self):
        return str(self.__dict__)

    def to_csv(self, separator = ","):
        line = ""
        for key in self.__dict__.keys():
            line += str(self.__dict__[key]) + separator
        return line

def get_books(your_key):
    urlbase = "https://www.goodreads.com/book/show/"
    params = { 
        "key" : your_key,
        "format" : "xml"
    }
    last_book = 6#00000000 # 44441958
    loop_step = 1#1000000
    books = []
    error = {}
    for book_id in range(1, last_book, loop_step):
        url = urlbase + str(book_id)
        print(url)
        r = requests.get(url, params = params)
        if (r.status_code == 200):
            try:
                books.append(Book(ET.fromstring(r.text)))
            except Exception as e:
                error[book_id] = e
        else:
            error[book_id] = r.status_code
        time.sleep(1)
    return books, error

def write_to_csv(books, filename="books.csv", delimiter=","):
    f = open(filename, "w") 
    w = csv.DictWriter(f, Book.headers, delimiter=delimiter)
    for book in books:
        w.writerow(book.__dict__)
    f.close()

def read_book(filename="book1.xml"):
    f = open(filename, "r")
    book = Book(ET.parse(f))
    return [book], {}

# books, error = get_books(key)
books, error = read_book()
write_to_csv(books, delimiter=",")
print(error)
