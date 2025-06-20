# Spotify to Yandex Music Transfer Tool
🚀 Утилита для переноса плейлистов и любимых треков из Spotify в Яндекс.Музыку

*Работает в асинхронном режиме и поддерживает одновременную обработку нескольких пар аккаунтов.*
# 🔍 О проекте
Используемые библиотеки:

* Неофициальная библиотека ```yandex-music-api``` для работы с API Яндекс Музыки с открытым исходным кодом от MarshalX ([ссылка](https://github.com/MarshalX/yandex-music-api/)).
* Официальная библиотека ```spotipy``` для работы с API Spotify ([ссылка](https://github.com/spotipy-dev/spotipy)).
* Selenium ([ссылка](https://www.selenium.dev/))

Функционал:

✔ Перенос любимых треков (как плейлист или как добавление в понравившиеся)

✔ Перенос плейлистов

✔ Асинхронная обработка аккаунтов парами

# ⚙️ Технологии
* Python 3.8+
* Библиотеки:
  ```
  selenium==4.9.0
  yandex_music
  spotipy
  webdriver_manager
  ```
  Протестировано на версиях:
  ```
  Python 3.8.10, 3.9.7, 3.13.4
  selenium==4.9.0
  yandex_music==2.2.0
  spotipy==2.25.1
  webdriver_manager==4.0.2
  ```
# 🛠 Установка и запуск
## Установка и настройка
  1. Установите Python
  2. Клонируйте репозиторий
  3. Создайте своё приложение в Spotify ([ссылка](https://developer.spotify.com/))
  4. В поле ```Redirect URIs``` укажите ```http://127.0.0.1/```
  5. При необходимости добавьте сторонних пользователей, которые смогут иметь доступ к приложению
  6. Вставьте ```Client ID``` в файле ```main.py```:
     ```python
     client_id = "your_client_id"
     ```
## Запуск
* Через ```run.bat```
* Через консоль:
  
  1. Установите зависимости:
     ```bash
     cd SpotifyToYMTransfer
     pip install -r requirements.txt
     ```
  2. Запустите программу:
     ```bash
     python main.py
     ```
# 🚀 Использование
1. Введите количество пар "Spotify-Яндекс" аккаунтов
2. Выполните вход в аккаунты
3. Следуйте подсказкам по выбору плейлистов для переноса в ходе работы программы

# ⚠️ Ограничения
* Только для Chrome
* Во избежание блокировки аккаунта Яндексом установлены задержки действий
* В Яндекс Музыке могут отсутствовать некоторые треки - программа об этом уведомит

# 🔗 Ссылки:
* [Yandex Music API Docs](https://yandex-music.readthedocs.io/en/main/ "API documentation")
* [Spotipy API Docs](https://spotipy.readthedocs.io/en/2.25.1/#getting-started "API documentation")



