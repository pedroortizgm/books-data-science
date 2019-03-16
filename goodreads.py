import requests
import xml.etree.ElementTree as ET
import time
import csv

class Book(object):
    def __init__(self, elementTree):
        et = elementTree.find('book')

        self.id = et.find('id').text
        self.isbn = et.find('isbn').text
        self.author = ""
        self.title = et.find('title').text
        self.isbn13 = et.find("isbn13").text
        #<asin></asin>
        #<kindle_asin></kindle_asin>
        # <marketplace_id></marketplace_id>
        # <country_code>ES</country_code>
        # <publication_year>2006</publication_year>
        # <publication_month>9</publication_month>
        # <publication_day>16</publication_day>
        # <publisher>Scholastic Inc.</publisher>
        # <language_code>eng</language_code>
        # <is_ebook>false</is_ebook><description>
 
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
        "key" : your_key 
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
    w = csv.DictWriter(f, ["id", "isbn", "author", "title", "isbn13"], delimiter=delimiter)
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
