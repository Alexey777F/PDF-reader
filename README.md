 # PDF-reader
 * Приложение с графическим интерфейсом для открытия pdf файлов 
 ___
 * GUI application for opening pdf files

![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/PDF-reader-screen.png)

## Описание - description
 * Приложение для чтения pdf файлов.
 * Возможность нарисовать прямоугольник красного цвета - Лкм в точку где хотите начать рисовать прямоугольник, далее Пкм в точку где хотите завершить рисование
 * Перелистывание организовано в формате "карусели", при нажатии на кнопку назад на первой странице - отображается последняя и наоборот если на последней нажать вперед - отобразится первая страница
 * Возможность сохранить изображение текущей отображаемой страницы в формате png
 * Версия 2.0 что нового:
   - Логика разделения pdf файла добавлена на сервер
   - Добавлен сервер NGINX который проксирует все запросы от приложения на сервер
   - Добавлена возможность сохранить изображение текущей отображаемой страницы в формате png
   - Добавлен docker-compose.yml и Dockerfile для установки серверов, библиотек и логики в контейнеры
 ___
 * Application for reading pdf files.
 * Ability to draw a red rectangle - LMB at the point where you want to start drawing the rectangle, then RMB at the point where you want to finish drawing
 * Flipping is organized in a “carousel” format; when you press the back button on the first page, the last page is displayed, and vice versa, if you press forward on the last page, the first page is displayed
 * Ability to save the image of the currently displayed page in png format
 * Version 2.0 what's new:
   - Logic for splitting a pdf file has been added to the server
   - Added NGINX server that proxies all requests from the application to the server
   - Added the ability to save the image of the currently displayed page in png format
   - Added docker-compose.yml and Dockerfile for installing servers, libraries and logic in containers

## Технологии - Technologies
 * Docker-compose
 * Python(docker image): 3.9.18-bullseye
 * Nginx(docker image)
 * Flask(v. 2.3.2)
 * PyQt5(v. 5.15.7)
 * requests(v. 2.31.0)
 * PyMuPDF(v. 1.23.7)

## Установка с помощью Docker-compose - Install with Docker-compose
 * Установите Docker Desktop под вашу ОС
 * Необходимо скопировать все содержимое директории v2.0_with_server в отдельный каталог.
 * Зайдите в директорию server
 * Запустите сборку образов и создания контейнеров с помощью команды: docker-compose up --build
 * Ваша серверная часть запущена
 * Зайдите в директорию client и запустите команду pip install -r requirements.txt
 * Запустите команду запуска файла main.py командой python3 main.py
 ___
 * Install Docker Desktop on your OS
 * It is necessary to copy all the contents of the v2.0_with_server directory to a separate directory.
 * Go to the server directory
 * Start building images and creating containers using the command: docker-compose up --build
 * Your backend is running
 * Go to the client directory and run the command pip install -r requirements.txt
 * Run the main.py file run command with python3 main.py command

## Как работает - How does it works
  * Примеры работы приложения
  * Application examples
![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/PDF-reader.gif)
  * Схема работы приложения
  * Scheme of application
![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/scheme_PDF_reader.png)



