 # PDF-reader
 * Описание 
 ___
 * Decription
![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/PDF-reader-screen.png)
## Технологии - Technologies
 * Docker-compose
 * Python(image): 3.9.18-bullseye
 * Flask(v. 2.3.2)
 * PyQt5(v. 5.15.7)
 * requests(v. 2.31.0)
 * PyMuPDF(v. 1.23.7)

## Установка с помощью Docker-compose - Install with Docker-compose
 * Установите Docker Desktop под вашу ОС
 * Необходимо скопировать все содержимое репозитория в отдельный каталог.
 * Установите виртуальное окружение на вашей ОС, на Mac OS python3 -m venv my_env
 * Активируйте виртуальное окружение на вашей ОС, на Mac OS source my_env/bin/activate
 * Запустите сборку образа и создания контейнера с помощью команды: docker-compose up --build
 * Приложение запущено в контейнере app_container 
 ___
 * Install Docker Desktop on your OS
 * It is necessary to copy all important repositories to a separate directory.
 * Install a virtual environment on your OS, on Mac OS python3 -m venv my_env
 * Activate the virtual environment in your OS, in the Mac OS source my_env/bin/activate.
 * Start building the image and creating the container using the command: docker-compose up --build
 * The application is running in the app_container container
   
## Как работает - How does it works
  * Примеры работы приложения
  * Application examples
![PDF-reader](https://github.com/Alexey777F/PDF-reader/blob/main/PDF-reader.gif)

