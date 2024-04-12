import csv
import sys
from urllib.parse import urljoin
from functions import *

# Global variables
fields = ["product_page_url",
          "universal_product_code (upc)",
          "title",
          "price_including_tax",
          "price_excluding_tax",
          "number_available",
          "product_description",
          "category",
          "review_rating",
          "image_url"]
data_folder_ = "scrapped"


def get_product_information(table):
    """
    Parse the content of HTML table containing the book's information and store them into a Dict. Return only the
    value needed for the project.
    :param table: BeautifulSoup with the content of an HTML table, consisting of the book's information.
    :return: "UPC" value, "Price (incl. tax)" value, "Price (excl. tax)" value, "Availability" value.
    """
    data = {}
    for table_row in table.find_all("tr"):
        data[table_row.th.string] = table_row.td.string
    return data["UPC"], data["Price (incl. tax)"], data["Price (excl. tax)"], availability_to_number(
        data["Availability"])


def save_cover(image_url, category, book_url):
    """
    Takes the images information and save the image.
    :param image_url: Url of the image.
    :param category: Category of the book used for the saving folder.
    :param book_url: Url of the book used for naming the image file.
    """
    folder = data_folder + '/' + category
    filename = book_url.replace('https://books.toscrape.com/catalogue/', '').replace('/index.html', '')
    filename = filename + '.jpg'
    img_data = requests.get(image_url).content
    create_data_folder(folder)
    with open(folder + '/' + filename, 'wb') as handler:
        handler.write(img_data)


def scrap_book_page(book_url):
    """
    Takes the url of a book and return its information parsed.
    Call the function to save the cover.
    :param book_url: Url of the book's page
    :return: Array containing the parsed and sorted information of the book.
    """
    book_soup = get_soup(book_url)
    product_page_url = book_url
    universal_product_code, price_including_tax, price_excluding_tax, number_available = get_product_information(
        book_soup.find(class_="table table-striped"))
    title = book_soup.find(class_="product_main").h1.string.strip()
    description_field = book_soup.find(id="product_description")
    if description_field:
        product_description = description_field.find_next("p").string.strip()
    else:
        product_description = ""
    category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].a.string.strip()
    review_rating = rating_to_number(book_soup.find(class_="star-rating").get("class"))
    image_url = urljoin(book_url, book_soup.img["src"])
    save_cover(image_url, category, book_url)
    return [product_page_url,
            universal_product_code,
            title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            product_description,
            category,
            review_rating,
            image_url]


def crawl_category_page(category_url, writer):
    """
    Takes the url of a category and call scrap_book_page() on every book found.
    Save the returned values of scrap_book_page() into the category's CVS file.
    Will crawl through the category pages until no more "Next button" is present.
    :param category_url: Url of the category.
    :param writer: Writer of the category's CVS.
    """
    while True:
        soup = get_soup(category_url)
        book_list = soup.find("section").find(class_="row").find_all("li")
        for book in book_list:
            book_url = urljoin(category_url, book.a.get('href'))
            writer.writerow(scrap_book_page(book_url))
        next_page = soup.find("li", class_="next")
        if not next_page:
            break
        category_url = urljoin(category_url, next_page.a.get('href'))


def crawl_all_categories(url):
    """
    Look for the categories url present in the page, create a CVS file and call the function crawl_category_page()
    on every category found.
    :param url: Url of the website,
    Accept "https://books.toscrape.com/" or "https://books.toscrape.com/catalogue/category/books_1/index.html"
    or similar structured website.
    :param data_folder: folder name or path used for saving.
    """
    create_data_folder(data_folder)
    soup = get_soup(url)
    category_list = soup.find(class_="nav nav-list").find("ul").find_all("li")
    for category in category_list:
        category_name = category.a.string.strip()
        with open(data_folder + '/' + category_name + '.csv', 'w', encoding='UTF-8', newline='') as file_csv:
            writer = csv.writer(file_csv, delimiter=',')
            writer.writerow(fields)
            category_url = urljoin(url, category.a.get('href'))
            crawl_category_page(category_url, writer)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    crawl_all_categories("https://books.toscrape.com/")
