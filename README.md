 # PDF-reader
 * Приложение с графическим интерфейсом для открытия pdf файлов 
 ___
 * GUI application for opening pdf files

![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/PDF-reader-screen.png)

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



