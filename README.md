# Космический телеграм-бот

### Загрузчик фоток космоса в Telegram

Скрипт автоматически собирает фотографии космоса с сайтов [spacex.com](https://www.spacex.com/) и [nasa.gov](https://www.nasa.gov/?kscnasa.rm). Бот публикует эти фотографии на твоём телеграм канале,  для этого бот нужно назначить администратором канала.

Программа берет настройки из нестандартных переменных окружения. Перед запуском программы создаём фаил `.env` и ложим туда свой Nasa API ключ, токен телеграм бота который нужно создать и id чата.
```python
NASA_API_KEY=nasa_api-key
TG_TOKEN=tg_token
TG_CHAT_ID=tg_chat_id
``` 
Без него программа не запустится.

Так же можно изменить периодичность публикации изменив значение переменной `time_sleep` (значение в секундах)
```python
def main():                                 
    sleep_time = 86400                      
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

### Пример запуска кода

```python
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://devman.org/).
 
