import os
import requests
from bs4 import BeautifulSoup
from word2number import w2n


def get_soup(url_to_soup):
    """
    Request the url content and return the page as BeautifulSoup.
    :param url_to_soup: String containing the url of the page.
    :return: BeautifulSoup object.
    """
    page = requests.get(url_to_soup)
    return BeautifulSoup(page.content, 'html.parser')


def create_data_folder(path):
    """
    Check if a folder exist, create it if it doesn't.
    :param path: String of the path to the file/folder.
    """
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)


def availability_to_number(availability):
    """
    Transform the string of the availability of a book into a number.
    Numbers in the string should only be number of books available.
    Example : "Available (10 books available)" will return 10
    :param availability: String detailing the availability of a book.
    :return: Number of book available.
    """
    return ''.join(x for x in availability if x.isdigit())


def rating_to_number(full_class):
    """
    Transform a spelled number in a number.
    Takes an array of string and return the second slot as a number.
    Example : ["", "Two"] will return 2.
    :param full_class: Array of strings, second slot is a spelled number.
    :return: Second slot as an int.
    """
    return w2n.word_to_num(full_class[1])
