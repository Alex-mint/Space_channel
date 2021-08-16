import os
import requests
import json
import time
import telegram

from os import listdir
from urllib.parse import urlparse
from dotenv import load_dotenv


def fetch_spacex_last_launch(url, path):
    response = requests.get(url)
    response.raise_for_status()
    links = json.loads(response.text)["links"]["flickr"]["original"]
    for link_number, link in enumerate(links):
        response = requests.get(link)
        with open(f"{path}spacex{link_number}.jpg", "wb") as file:
            file.write(response.content)


def get_extension(url):
    path, extension = os.path.splitext(url)
    return extension


def get_name(url):
    name, path = os.path.split(url)
    name = urlparse(url)
    return name.netloc


def get_images_links(nasa_url, nasa_api_key):
    payload = {
        "count": "30",
        "api_key": nasa_api_key
    }
    raw_response = requests.get(nasa_url, params=payload)
    response = json.loads(raw_response.text)
    images_links = []
    for link in response:
        images_links.append(link["url"])
    return images_links


def fetch_nasa_image(nasa_url, path, nasa_api_key):
    for link_number, link in enumerate(get_images_links(nasa_url, nasa_api_key)):
        if get_name(link) == "apod.nasa.gov":
            response = requests.get(link)
            extension = get_extension(link)
            with open(f"{path}nasa{link_number}{extension}", "wb") as file:
                file.write(response.content)


def fetch_epic_image(url, path, nasa_api_key):
    raw_response = requests.get(url)
    response = json.loads(raw_response.text)
    for image_number, image_data in enumerate(response):
        image_date = image_data["date"]
        image_name = image_data["image"]
        link = requests.get(make_epic_image_link(image_date, image_name, nasa_api_key))
        with open(f"{path}epic_nasa{image_number}.jpg", "wb") as file:
            file.write(link.content)


def make_epic_image_link(image_date, image_name, nasa_api_key):
    image_date = date_convertor(image_date)
    link = "https://api.nasa.gov/EPIC/archive/natural/" \
           + "{}/png/{}.png?api_key={}".format(image_date, image_name, nasa_api_key)
    return link


def date_convertor(image_date):
    converted_image_date = image_date.split()[0].replace("-", "/")
    return converted_image_date


def get_images_paths(images_directories):
    images_paths = []
    for images_dir in images_directories:
        images = listdir(images_dir)
        for image in images:
            image_path = image.replace(image, f"{images_dir}/{image}")
            images_paths.append(image_path)
    return images_paths


def send_picture_to_telegram(images_paths, tg_token):


    bot = telegram.Bot(token=tg_token)
    while True:
        for path in images_paths:
            bot.send_document(chat_id="@best_space_images",
                              document=open(path, "rb"))
            time.sleep(86400)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    nasa_api_key = os.getenv("NASA_API_KEY")
    images_directories = ["spacex_images", "nasa_images", "nasa_epic_images"]
    spacex_path = "spacex_images/"
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"
    nasa_path = "nasa_images/"
    nasa_epic_path = "nasa_epic_images/"
    nasa_url = "https://api.nasa.gov/planetary/apod"
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/" \
                    + "natural/images?api_key={}".format(nasa_api_key)
    try:
        os.makedirs("spacex_images")
        os.makedirs("nasa_images")
        os.makedirs("nasa_epic_images")
    except FileExistsError:
        None
    fetch_spacex_last_launch(spacex_url, spacex_path)
    fetch_nasa_image(nasa_url, nasa_path, nasa_api_key)
    fetch_epic_image(nasa_epic_url, nasa_epic_path, nasa_api_key)
    images_paths = get_images_paths(images_directories)
    send_picture_to_telegram(images_paths, tg_token)


if __name__ == "__main__":
    main()
