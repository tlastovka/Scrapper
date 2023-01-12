import string
from bs4 import BeautifulSoup
import requests
import os
import os.path

'''
Inputs:
'''


def get_clean_title(title):
    """Remove punctuation and replace space for _"""
    return title.translate(str.maketrans("", "", string.punctuation)).replace(" ", "_")


# To generate a list of URLs corresponding to to respective number of pages
base_url = str("https://www.nature.com/nature/articles?sort=PubDate&year=2020")
num_of_pages = int(
    input())  # https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=2
type_of_article = str(input())
Pages = {}
Page_N = {}
Pages[0] = base_url
x = 0

for page in range(2, num_of_pages + 1):
    Pages[page - 1] = f"{base_url}&page={page}"
for i in Pages:
    print(Pages[i])

# To generate directories with specific names "Page_N", where N is the page number
list_of_directories = []
for i in range(1, num_of_pages + 1):
    dir_entry = f"Page_{i}"
    list_of_directories.append(dir_entry)

print("List of directories", list_of_directories)

# Search and collect all articles on respective page and save each page with articles into the "articles" list

for n in range(0, num_of_pages):
    # print("n= ", n)
    # print("Pages_N= ", Pages[n])
    actual_url = Pages[n]

    # Directory
    directory = f"Page_{n + 1}"
    print(directory)
    # Parent Directory path
    parent_dir = "C:\\1. MySoft\\PyProjects\\Web Scraper\\Web Scraper\\task\\"
    print("Parent directory = ", parent_dir)
    # Path
    path = os.path.join(parent_dir, directory)

    # Create the directory
    os.mkdir(path)
    print("Directory '% s' created" % directory)

    # Create a page content object for all "directories", resp "pages"
    page_scan = requests.get(url=actual_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    # print("Page scan = ", page_scan.content)
    soup = BeautifulSoup(page_scan.content, 'html.parser')
    articles = (soup.find_all("article"))

    # We now have all articles on respective pages in a list called articles.

    if page_scan.status_code != 200:
        print("The URL returned ", page_scan.status_code)
    elif page_scan.status_code == 404:
        print("The URL returned ", page_scan.status_code)
    else:
        for article in articles:

            if article.find("span", {
                "class": "c-meta__type"}).text == type_of_article:  # AttributeError: ResultSet object has no attribute 'find'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?

                required_title = article.a.text
                required_link = article.a["href"]
                resp_art = requests.get(f"https://www.nature.com{required_link}")
                soup_art = BeautifulSoup(resp_art.content, "html.parser")
                article_body = soup_art.find(
                    "div", {"class": "c-article-body"}
                ).text.strip()
                #Page_N[n + 1] = article_body.encode()

                complete_name = os.path.join(path, f"{get_clean_title(required_title)}.txt")
                print("complete_name = ", complete_name)
                file = open(complete_name, "wb")
                file.write(article_body.encode())
                file.close()
                x = x + 1
