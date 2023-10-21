import os
import requests
from bs4 import BeautifulSoup
import string

# constants
base_url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
output = {}

# inputs
page_N = int(input())
article_type = input()

print(page_N, article_type)


def remove_punctuation(input_string):
    # Create a translation table
    translator = str.maketrans('', '', string.punctuation)

    # Use the translation table to remove punctuation
    clean_string = input_string.translate(translator)

    return clean_string

def is_requested_article_type(article):
    # check if article is of given article_type
    for tag in article.find_all('span'):
        if tag.has_attr('data-test') and tag.span.string == article_type:
            return True
    return False


def process_articles_in_page (page_soup):
    for article in page_soup.find_all('article'):
        # go over article's for a page
        if is_requested_article_type(article):
            title = str(article.a.contents[0])
            filename = remove_punctuation(title).replace(' ','_') + '.txt'
            for link in article.find_all('a'):
                article_url = 'https://www.nature.com' + link.get('href')
                print(article_url)
                article_soup = BeautifulSoup(requests.get(article_url).content, 'html.parser')
                article_teaser = str(article_soup.find("p", attrs={"class": "article__teaser"}).contents[0])

                file = open(filename, 'w', encoding='utf-8')
                file.write(article_teaser)
                file.close()
                print('Written ', filename)

# main loop
root = os.getcwd()
for page_nr in range(1, page_N + 1):
    r = requests.get(base_url + '&page=' + str(page_nr))
    page_soup = BeautifulSoup(r.content, 'html.parser')
    os.mkdir(root + '/Page_' + str(page_nr))
    os.chdir('Page_' + str(page_nr))
    process_articles_in_page(page_soup)
    os.chdir(root)
