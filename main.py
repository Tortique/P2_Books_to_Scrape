import csv

import requests
from bs4 import BeautifulSoup


def page_scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    en_tete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
               'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
               'image_url']

    with open('data/page.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(en_tete)

        upc = soup.find(text="UPC").parent.parent.find("td").string
        title = soup.find("h1").string
        pit = soup.find(text="Price (incl. tax)").parent.parent.find("td").string
        pet = soup.find(text="Price (excl. tax)").parent.parent.find("td").string
        number = soup.find(text="Availability").parent.parent.find("td").string
        description = soup.find("meta", {"name": "description"})['content'].removeprefix(
            "\n   ").removesuffix("\n")
        categoryLists = soup.find_all("li")
        category = categoryLists[2].find("a").string
        review_rating = soup.find(class_="star-rating")['class'][1]
        image_url = soup.find("img")['src'].replace("../../", "http://books.toscrape.com/")

        info = [url, upc, title, pit, pet, number, description, category, review_rating, image_url]
        writer.writerow(info)

page1 = page_scrap("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")


