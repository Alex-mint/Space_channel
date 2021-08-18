# Космический телеграм-бот

### Загрузчик фоток космоса в Telegram

Скрипт автоматически собирает фотографии космоса с сайтов [spacex.com](https://www.spacex.com/) и [nasa.gov](https://www.nasa.gov/?kscnasa.rm). Бот публикует эти фотографии на твоём телеграм канале,  для этого бот нужно назначить администратором канала.

Программа берет настройки из нестандартных переменных окружения. Перед запуском программы создаём фаил `.env` и ложим туда свой Nasa API ключ и токен телеграм бота который нужно создать.
```python
NASA_API_KEY=nasa_api-key
TG_TOKEN=tg_token
``` 
Без него программа не запустится.

Так же можно изменить периодичность публикации изменив значение переменной `time_sleep` (значение в секундах)
```python
def main():                                 
    time_sleep = 86400                      
    load_dotenv()                           
    tg_token = os.getenv("TG_TOKEN")        
    nasa_api_key = os.getenv("NASA_API_KEY")
```

### Как установить

Python3 должен быть уже установлен.
Затем используете `pip` (или `pip3` , если есть конфликт с Python2) для установки зависимостей: 
```python
pip install - r requirements.txt
```

### Примерно запуска кода

```python
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
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://devman.org/).
 
