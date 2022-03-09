import csv
import os

import requests
from bs4 import BeautifulSoup


def page_scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    upc = soup.find(text="UPC").parent.parent.find("td").string
    title = soup.find("h1").string
    pit = soup.find(text="Price (incl. tax)").parent.parent.find("td").string
    pet = soup.find(text="Price (excl. tax)").parent.parent.find("td").string
    number = soup.find(text="Availability").parent.parent.find("td").string
    description = soup.find("meta", {"name": "description"})['content'].removeprefix(
        "\n   ").removesuffix("\n")
    categorises = soup.find_all("li")
    category = categorises[2].find("a").string
    review_rating = soup.find(class_="star-rating")['class'][1]
    image_url = soup.find("img")['src'].replace("../../", "http://books.toscrape.com/")

    info = [url, upc, title, pit, pet, number, description, category, review_rating, image_url]
    return info


def category_scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
              'image_url']
    name = soup.find("h1").string

    if not os.path.isdir('data'):
        os.mkdir('data')

    if not os.path.isdir('data/' + name):
        os.mkdir('data/' + name)
        os.mkdir('data/' + name + '/images')

    with open('data/' + name + '/' + name + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)

        books = soup.find_all("div", class_="image_container")

        isnext = soup.find("li", class_="next")
        while isnext:
            url = url.removesuffix("index.html") + isnext.find("a")["href"]
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            books.extend(soup.find_all("div", class_="image_container"))
            isnext = soup.find("li", class_="next")

        for book in books:
            url = "http://books.toscrape.com/catalogue/" + book.a["href"].removeprefix("../../../")
            info = page_scrap(url)
            writer.writerow(info)
            image = requests.get(info[-1])
            with open("data/" + name + "/images/" + info[2].replace(':', '').replace('/','').replace('\\' , '' ).replace('"', '').replace('.', '').replace('*', '').replace('?','') + ".jpg", 'wb') as f:
                f.write(image.content)


def scraper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    categories = soup.find("ul", class_="nav").find("ul").find_all("a")
    for category in categories:
        print(category["href"])
        category_scrap(url + category["href"])


scraper("https://books.toscrape.com/")
