***
## Инструкция по эксплуатации проекта
***

### Перечень файлов проекта и краткое описание.
***
### админ-панель Django для фриланс-бота.
***

### Файлы в корне проекта:

1. __.gitignore__ - файл сообщающий git, не отслеживать определенные файлы и директории .
2. __manage.py__ - файл с командами приложения.
3. __requirements.txt__ - файл с зависимостями.
4. __readme.md__ - инструкция по эксплуатации проекта.


### Пакеты и директории в корне проекта:

#### 1. top_laptop:
* __init.py__ - инициализирует пакет top_laptop и его содержимое.
* __asgi.py__ - файл для ассинхронной связи сервера и проекта.
* __wsgi.py__ - файл для связи сервера и проекта.
* __settings.py__ - файл с конфигурациями проекта.
* __urls.py__ - файл с URL-адресами проекта.

#### 2. app_laptop:
* __init.py__ - инициализирует пакет top_laptop и его содержимое.
* __admin.py__ - файл с настройками админ-панели.
* __apps.py__ - файл с конфигурацией приложения.
* __models.py__ - файл с моделями базы данных приложения.
    #### 1. migrations:
    * __init.py__ - инициализирует пакет migrations и его содержимое

#### 3. config:
* __gunicorn.conf.py__ - файл с конфигурациями гуникорна.
* __i_want.conf__ - файл с конфигурациями супервизора.

#### 4. logs:
* __debug.log__ - файл с логами проекта.

***
### Деплой проекта на linux debian

Для начала необходимо прописать настройки в файлах: settings.py(хост, секретный ключ и данные для БД, 
gunicorn.conf.py(ip-адрес и имя пользователя), i_want.conf(пути до лог файла, гуникорна и wsgi файла).

Далее необходимо на удобном для вас сервисе приобрести сервер.

Создаём в командной строке SSH ключ: ssh-keygen -t rsa -b 2048 -C <имя ключа> -f <имя ключа>

Добавляем ключ на приобретенный ранее сервер.

Логинимся: ssh root@<ip-адрес сервера>

Обновляем систему командами: apt update, apt upgrade

Добавляем нового пользователя: adduser <имя пользователя>

Даём пользователю рутовские права: usermod -aG sudo <имя пользователя>

Переключаемся на нового пользователя: su <имя пользователя>

Устанавливаем програмное обеспечение: sudo apt install nginx git supervisor

Устанавливаем venv для создания виртуального окружения: apt-get install python3-venv

Создаём виртуальное окружение: python3 -m venv venv

Активируем окружение: source venv/bin/activate

Клонируем проект с Вашего репозитория: git clone <адрес репозитория>

Переходим в папку проекта: cd <имя директории проекта>

Устанавливаем зависимости: pip install -r requirements.txt

Если возникнут проблемы с установкой, то дополнительно устанавливаем компиляции и повторяем установку зависимостей:

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev

sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm

sudo apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev

Создаём миграции (так же в директории проекта): python manage.py makemigrations

Применяем миграции: python manage.py migrate

Устанавливаем gunicorn: gunicorn <директория проекта>.wsgi:application --bind <ip-адрес сервера>:8000

Настраиваем nginx (Откроется файл кончигурации nginx): sudo nano /etc/nginx/sites-available/default

Стираем все данные в файле: alt+t


server {

    listen 80;

    server_name 111.222.333.44; # здесь прописать или IP-адрес или доменное имя сервера

    access_log  /var/log/nginx/example.log; 
 
    location /static/ {
        root /home/user/myprojectenv/myproject/myproject/; #Прописать путь до диретории статик в проекте
        expires 30d;
    }
 
    location / {
        proxy_pass http://127.0.0.1:8000; 
        proxy_set_header Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}

Выходим из nano редактора: ctrl + x
Сохраняем файл: y
Подтверждаем: Enter

Перезапускаем nginx: sudo service nginx restart

Настраиваем supervisor (Переходим в директорию): cd /etc/supervisor/conf.d/

Добавляем в директорию ссылку на файл настроек supervisor: sudo ln <путь до файла>

Активируем supervisor: sudo update-rc.d supervisor enable

Стартуем supervisor: sudo service supervisor start

Подтягиваем файл конфигурации supervisor: sudo supervisorctl reread

Добавляем данный файл в процесс: sudo supervisorctl update

Проверяем статус запущенных процессов: sudo supervisorctl status

После выполнения алгоритма проект будет запущен на Gunicorn, а supervisor не даст ему упасть.

Дополнительные команды:

Перезапуск процесса: sudo supervisorctl restart <имя проекта>

Остановка процесса: sudo supervisorctl stop <имя проекта>

Запуск процесса: sudo supervisorctl start <имя проекта>