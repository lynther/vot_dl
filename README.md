## VOT_DL

Скрипт позволяющий переводить видео через "yandex voice over translation" и сохранять их локально объединяя аудиодорожки.

По сути это тоже самое что и скрипт [Powershell by Dragoy](https://github.com/FOSWLY/vot-cli/tree/main/scripts) только поддерживающий одновременный перевод до 20 видео и больше, в зависимости от настроек.

## Установка

Для работы требуется python >=3.5 и ffmpeg (для объединения аудио дорожек)

```bash
git clone https://github.com/lynther/vot_dl.git
pip install -r requirements.txt
```

## Использование

Перед запуском нужно создать файл urls.txt рядом со скриптом.

А так же предварительно заполнить его ссылками на видео.

!**Ссылки на видео должны находиться в открытом доступе что бы сервис яндекса смог к ним обращаться по сети.**!

```
python main.py
```

![example](https://github.com/lynther/vot_dl/blob/main/img/example.png "example")

## TODO

1. Сделать более удобный способ установки настроек
2. Добавить поддержку прокси для yt_dlp
