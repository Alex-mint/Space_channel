import os
import requests
import time
import telegram
from os import listdir
from urllib import parse
from dotenv import load_dotenv


def fetch_spacex_last_launch_images(path):
    image_name = "spacex"
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()["links"]["flickr"]["original"]
    download_images(path, links, image_name)


def get_extension(url):
    unquoted_url = parse.unquote(url)
    path = parse.urlparse(unquoted_url).path
    extension = os.path.splitext(path)[-1]
    return extension


def get_image_links(nasa_url, nasa_api_key):
    links_number = 30
    payload = {"count": str(links_number), "api_key": nasa_api_key}
    response = requests.get(nasa_url, params=payload)
    response.raise_for_status()
    response = response.json()
    image_links = [link["url"] for link in response]
    return image_links


def download_images(path, links, image_name, payload=None):
    path = os.path.join(path, image_name)
    for link_number, link in enumerate(links):
        extension = get_extension(link)
        response = requests.get(link, params=payload)
        response.raise_for_status()
        with open(f"{path}{link_number}{extension}", "wb") as file:
            file.write(response.content)


def fetch_nasa_images(path, nasa_api_key):
    image_name = "nasa"
    nasa_url = "https://api.nasa.gov/planetary/apod"
    nasa_image_links = get_image_links(nasa_url, nasa_api_key)
    for link in nasa_image_links:
        if parse.urlparse(link).netloc != "apod.nasa.gov":
            nasa_image_links.remove(link)
    download_images(path, nasa_image_links, image_name)


def fetch_epic_images(path, nasa_api_key):
    payload = {"api_key": nasa_api_key}
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(nasa_epic_url, params=payload)
    response.raise_for_status()
    response = response.json()
    links = []
    for image in response:
        image_date = image["date"]
        image_name = image["image"]
        link = make_epic_image_link(image_date, image_name)
        links.append(link)
    image_name = "epic"
    download_images(path, links, image_name, payload=payload)


def make_epic_image_link(
    image_date,
    image_name,
):
    image_date = image_date.split()[0].replace("-", "/")
    link = "https://api.nasa.gov/EPIC/archive/natural/" \
        f"{image_date}/png/{image_name}.png"
    return link


def get_image_paths(image_directories):
    all_image_paths = []
    for images_dir in image_directories:
        images = listdir(images_dir)
        image_paths = [f"{images_dir}/{image}" for image in images]
        all_image_paths += image_paths
    return all_image_paths


def send_pictures_to_telegram(image_paths, tg_token, tg_chat_id, sleep_time):
    bot = telegram.Bot(token=tg_token)
    while True:
        for path in image_paths:
            with open(path, "rb") as file:
                bot.send_document(chat_id=tg_chat_id, document=file)
                time.sleep(sleep_time)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    nasa_api_key = os.getenv("NASA_API_KEY")

    sleep_time = 86400
    image_directories = ["spacex_images", "nasa_images", "epic_images"]

    for directory in image_directories:
        os.makedirs(directory, exist_ok=True)

    spacex_path = "spacex_images"
    nasa_path = "nasa_images"
    nasa_epic_path = "epic_images"

    fetch_spacex_last_launch_images(spacex_path)
    fetch_nasa_images(nasa_path, nasa_api_key)
    fetch_epic_images(nasa_epic_path, nasa_api_key)

    image_paths = get_image_paths(image_directories)
    send_pictures_to_telegram(image_paths, tg_token, tg_chat_id, sleep_time)


if __name__ == "__main__":
    main()
