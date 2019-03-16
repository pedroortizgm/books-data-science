import requests
import xml.etree.ElementTree as ET
import time
import csv

class Book(object):
    headers = ["id", "isbn", "author", "title", "isbn13", "asin", "kindle_asin", "marketplace_id", "country_code", 
        "publication_date", "publisher", "language_code", "is_ebook", "books_count", "best_book_id", "reviews_count", 
        "ratings_sum", "ratings_count", "text_reviews_count", "original_publication_date", "original_title", "media_type", 
        "num_ratings_5", "num_ratings_4", "num_ratings_3", "num_ratings_2", "num_ratings_1"]

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
        self.publication_date = "/".join([et.find("publication_year").text, et.find("publication_month").text, et.find("publication_day").text])
        self.publisher = et.find("publisher").text
        self.language_code = et.find("language_code").text
        self.is_ebook = et.find("is_ebook").text
        work = et.find("work")
        self.books_count = work.find("books_count").text
        self.best_book_id = work.find("best_book_id").text
        self.reviews_count = work.find("reviews_count").text
        self.ratings_sum = work.find("ratings_sum").text
        self.ratings_count = work.find("ratings_count").text
        self.text_reviews_count = work.find("text_reviews_count").text
        self.original_publication_date = "/".join([work.find("original_publication_year").text, work.find("original_publication_month").text, work.find("original_publication_day").text]) 
        self.original_title = work.find("original_title").text
        self.media_type = work.find("media_type").text
        num_ratings = work.find("rating_dist").text.split("|")
        self.num_ratings_5 = num_ratings[0].split(":")[1]
        self.num_ratings_4 = num_ratings[1].split(":")[1]
        self.num_ratings_3 = num_ratings[2].split(":")[1]
        self.num_ratings_2 = num_ratings[3].split(":")[1]
        self.num_ratings_1 = num_ratings[4].split(":")[1]
 
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
    w.writeheader()
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
