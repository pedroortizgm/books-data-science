import requests
import xml.etree.ElementTree as ET
import time
import csv
import os
import sys, getopt
from dotenv import load_dotenv


class Book(object):
    def __init__(self, elementTree):
        et = elementTree.find('book')

        self.id = et.find('id').text
        self.isbn = et.find('isbn').text
        self.title = et.find('title').text
        self.isbn13 = et.find("isbn13").text
        self.asin = et.find("asin").text
        self.kindle_asin = et.find("kindle_asin").text
        self.marketplace_id = et.find("marketplace_id").text
        self.country_code = et.find("country_code").text
        self.publication_date = "/".join(
            [et.find("publication_year").text, et.find("publication_month").text, et.find("publication_day").text])
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
        self.original_publication_date = "/".join(
            [work.find("original_publication_year").text, work.find("original_publication_month").text,
             work.find("original_publication_day").text])
        self.original_title = work.find("original_title").text
        self.media_type = work.find("media_type").text
        num_ratings = work.find("rating_dist").text.split("|")
        self.num_ratings_5 = num_ratings[0].split(":")[1]
        self.num_ratings_4 = num_ratings[1].split(":")[1]
        self.num_ratings_3 = num_ratings[2].split(":")[1]
        self.num_ratings_2 = num_ratings[3].split(":")[1]
        self.num_ratings_1 = num_ratings[4].split(":")[1]
        self.average_rating = et.find("average_rating").text
        self.num_pages = et.find("num_pages").text
        self.format = et.find("format").text
        self.edition_information = et.find("edition_information").text
        self.ratings_count_global = et.find("ratings_count").text
        self.text_reviews_count_global = et.find("text_reviews_count").text
        self.authors = []
        self.illustrator = []
        self.contributor = []
        self.editor = []
        self.translator = []
        self.narrator = []
        for a in et.find("authors"):
            author = a.find("name").text 
            role = a.find("role").text          
            if (role is None): 
                self.authors.append(author)
            elif (role == 'Illustrator'):
                self.illustrator.append(author)
            elif (role == 'Contributor'): 
                self.contributor.append(author)
            elif (role == 'Editor'):
                self.editor.append(author)
            elif (role == 'Translator'):
                self.translator.append(author)
            elif (role == 'Narrator'):
                self.narrator.append(author)
            else:
                print("found role " + role + " on book " + self.id)
        self.authors.sort()
        self.authors = ",".join(self.authors)
        self.illustrator.sort()
        self.illustrator = ",".join(self.illustrator)
        self.contributor.sort()
        self.contributor = ",".join(self.contributor)
        self.editor.sort()
        self.editor = ",".join(self.editor)
        self.translator.sort()
        self.translator = ",".join(self.translator)
        self.narrator.sort()
        self.narrator = ",".join(self.narrator)

        # find from the popular shelves, if people wants to read, is reading or have already read the book
        self.read = 0
        for shelve in et.find("popular_shelves"):
            shelve_name = shelve.attrib["name"]
            shelve_value = int(shelve.attrib["count"])
            if (shelve_name == "to-read"):
                self.to_read = shelve_value
            elif (shelve_name == "currently-reading"):
                self.currently_reading = shelve_value
            else:
                if (shelve_name.find("read") > -1):
                    self.read += shelve_value

    def __repr__(self):
        return str(self.__dict__)

    def to_csv(self, separator=","):
        line = ""
        for key in self.__dict__.keys():
            line += str(self.__dict__[key]) + separator
        return line
    
    def write_to_csv(self, w):
        w.writerow(self.__dict__)


def get_books(your_key, writer, file, start, end, loop_step):
    urlbase = "https://www.goodreads.com/book/show/"
    params = {
        "key": your_key,
        "format":"xml"
    }
    error = {}
    for book_id in range(start, end + 1, loop_step):
        url = urlbase + str(book_id)
        print(url)
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            try:
                book = Book(ET.fromstring(r.text))
                book.write_to_csv(writer)
            except Exception as e:
                error[book_id] = e
        else:
            error[book_id] = r.status_code
        time.sleep(1)
    file.close()
    return error


def create_csv(filename="books.csv", delimiter=","):
    headers = ["id", "isbn", "title", "isbn13", "asin", "kindle_asin", "marketplace_id", "country_code",
               "publication_date", "publisher", "language_code", "is_ebook", "books_count", "best_book_id",
               "reviews_count",
               "ratings_sum", "ratings_count", "text_reviews_count", "original_publication_date", "original_title",
               "media_type",
               "num_ratings_5", "num_ratings_4", "num_ratings_3", "num_ratings_2", "num_ratings_1",
               "average_rating", "num_pages", "format", "edition_information", "ratings_count_global",
               "text_reviews_count_global", "authors", 'illustrator', 'contributor', 'editor', 'translator', 'narrator', 
               "to_read", "read", "currently_reading"]

    f = open(filename, "a+")
    w = csv.DictWriter(f, headers, delimiter=delimiter)
    if (os.stat(filename).st_size == 0):
        w.writeheader()
    return w, f

def load_books(filename, start, end, loop_step):
    writer, f = create_csv(filename)
    error = get_books(API_KEY, writer, f, start, end, loop_step)
    print(error)

def read_book(inputfile = "book1.xml", outputfile = "book.csv"):
    writer, f = create_csv(outputfile)
    try:
        book = Book(ET.parse(inputfile))
        book.write_to_csv(writer)
    except Exception as e:
        print(e)
    
def main(argv):
    output_file = "books.csv"
    input_file = None
    start = 1
    end = 2000
    loop_step = 1
    try:
        opts, args = getopt.getopt(argv, "hi:o:s:e:l:", ["ifile", "ofile"])
    except getopt.GetoptError:
        print('goodreads.py -o outputfile -i inputfile -s start -e end -l loop_step')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("goodreads.py -o outputfile -i inputfile -s start -e end -l loop_step")
            sys.exit()
        elif opt in ("-i", "--ifile"): # reads book from file
            input_file = arg
        elif opt in ("-o", "--ofile"): # writes into file
            output_file = arg
        elif opt in ("-s"):
            start = int(arg)
        elif opt in ("-e"):
            end = int(arg)
        elif opt in ("-l"):
            loop_step = int(arg)
    if (input_file is None): # not read book from file, so, run getbooks
        print("load books: " + output_file + " " + str(start) + " " + str(end) + " " + str(loop_step))
        load_books(output_file, start, end, loop_step)
    else:
        read_book(input_file, output_file)

if __name__ == "__main__":
    # Load .env variables
    load_dotenv()
    API_KEY = os.getenv("API_KEY", False)
    if not API_KEY:
        sys.exit("Error: API_KEY not found")
    main(sys.argv[1:])
