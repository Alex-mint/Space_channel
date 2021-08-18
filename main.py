import os
import requests
import json
import time
import telegram

from os import listdir
from urllib import parse
from dotenv import load_dotenv


def fetch_spacex_last_launch(path):
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()["links"]["flickr"]["original"]
    for link_number, link in enumerate(links):
        response = requests.get(link)
        response.raise_for_status()
        with open(f"{path}spacex{link_number}.jpg", "wb") as file:
            file.write(response.content)


def get_extension(url):
    unquoted_url = parse.unquote(url)
    path = parse.urlparse(unquoted_url).path
    extension = path.rstrip("/").split(".")[-1]
    return extension


def get_name(url):
    name, path = os.path.split(url)
    name = parse.urlparse(url)
    return name.netloc


def get_images_links(nasa_url, nasa_api_key):
    links_number = 30
    payload = {
        "count": str(links_number),
        "api_key": nasa_api_key
    }
    response = requests.get(nasa_url, params=payload).json()
    images_links = [link["url"] for link in response]
    return images_links


def fetch_nasa_image(path, nasa_api_key):
    nasa_url = "https://api.nasa.gov/planetary/apod"
    for link_number, link in enumerate(get_images_links(nasa_url, nasa_api_key)):
        if get_name(link) == "apod.nasa.gov":
            response = requests.get(link)
            response.raise_for_status()
            extension = get_extension(link)
            with open(f"{path}nasa{link_number}{extension}", "wb") as file:
                file.write(response.content)


def fetch_epic_image(path, nasa_api_key):
    payload = {"api_key": nasa_api_key}
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(nasa_epic_url, params=payload)
    response.raise_for_status()
    response = response.json()
    for image_number, image_data in enumerate(response):
        image_date = image_data["date"]
        image_name = image_data["image"]
        link = requests.get(make_epic_image_link(image_date, image_name),
                            params=payload)
        with open(f"{path}epic_nasa{image_number}.jpg", "wb") as file:
            file.write(link.content)


def make_epic_image_link(image_date, image_name,):
    image_date = image_date.split()[0].replace("-", "/")
    link = "https://api.nasa.gov/EPIC/archive/natural/" \
        f"{image_date}/png/{image_name}.png"
    return link


def get_images_paths(images_directories):
    images_paths = []
    for images_dir in images_directories:
        images = listdir(images_dir)
        images_paths = [f"{images_dir}/{image}" for image in images]
    return images_paths


def send_pictures_to_telegram(images_paths, tg_token, time_sleep):
    bot = telegram.Bot(token=tg_token)
    while True:
        for path in images_paths:
            bot.send_document(chat_id="@best_space_images",
                              document=open(path, "rb"))
            time.sleep(time_sleep)


def main():
    time_sleep = 86400
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    nasa_api_key = os.getenv("NASA_API_KEY")
    images_directories = ["spacex_images", "nasa_images", "nasa_epic_images"]
    spacex_path = "spacex_images/"
    nasa_path = "nasa_images/"
    nasa_epic_path = "nasa_epic_images/"
    os.makedirs("spacex_images", exist_ok=True)
    os.makedirs("nasa_images", exist_ok=True)
    os.makedirs("nasa_epic_images", exist_ok=True)
    fetch_spacex_last_launch(spacex_path)
    fetch_nasa_image(nasa_path, nasa_api_key)
    fetch_epic_image(nasa_epic_path, nasa_api_key)
    images_paths = get_images_paths(images_directories)
    send_pictures_to_telegram(images_paths, tg_token, time_sleep)


if __name__ == "__main__":
    main()
