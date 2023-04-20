# Сайт "Продуктовый помощник"

## Об авторе

Танхаев Данзан Леонидович  
Python-разработчик

E-mail: dtankhaev@gmail.com  
Telegram: @dtankhaev

51.250.20.19

email: root@gmail.com

password: mynameisroot

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=ffffff&color=043A6B)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=043A6B)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=ffffff&color=043A6B)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=ffffff&color=043A6B)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=ffffff&color=043A6B)](https://cloud.yandex.ru/)

## Описание

«Продуктовый помощник»
Сайт является - базой кулинарных рецептов. Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате. Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx

Документация к API доступна [здесь](http://51.250.20.19//api/docs/)

## Подготовка и запуск проекта

### Склонировать репозиторий на локальную машину:

```
git clone git@github.com:dtankhaev/foodgram-project-react.git
```

## Для работы с удаленным сервером (на ubuntu):

- Выполните вход на свой удаленный сервер

- Установите docker на сервер:

```
sudo apt install docker.io
```

- Установите docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
- Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

- Cоздайте .env файл и впишите:
  ```
  DB_ENGINE=<django.db.backends.postgresql>
  DB_NAME=<имя базы данных postgres>
  DB_USER=<пользователь бд>
  DB_PASSWORD=<пароль>
  DB_HOST=<db>
  DB_PORT=<5432>
  SECRET_KEY=<секретный ключ проекта django>
  ```
- Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

  ```
  DOCKER_PASSWORD=<пароль от DockerHub>
  DOCKER_USERNAME=<имя пользователя>

  SECRET_KEY=<секретный ключ проекта django>

  USER=<username для подключения к серверу>
  HOST=<IP сервера>
  PASSPHRASE=<пароль для сервера, если он установлен>
  SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

  TELEGRAM_TO=<ID чата, в который придет сообщение>
  TELEGRAM_TOKEN=<токен вашего бота>
  ```

  Workflow состоит из трёх шагов:

  - Проверка кода на соответствие PEP8
  - Сборка и публикация образа бекенда на DockerHub.
  - Автоматический деплой на удаленный сервер с применением миграций и сборки статики
  - Отправка уведомления в телеграм-чат.

- На сервере соберите docker-compose:

```
sudo docker-compose up -d --build
```

- После успешной сборки на сервере выполните команды (только после первого деплоя):
  - Создать суперпользователя Django:
  ```
  sudo docker-compose exec backend python manage.py createsuperuser
  ```
  - Проект будет доступен по вашему IP

## Регистрация и авторизация

В сервисе предусмотрена система регистрации и авторизации пользователей.
Обязательные поля для пользователя:

<li> Логин
<li> Пароль
<li> Email
<li> Имя
<li> Фамилия

## Права доступа к ресурсам сервиса

### неавторизованные пользователи могут:

    - создать аккаунт;
    - просматривать рецепты на главной;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;

### авторизованные пользователи могут:

    - входить в систему под своим логином и паролем;
    - выходить из системы (разлогиниваться);
    - менять свой пароль;
    - создавать/редактировать/удалять собственные рецепты;
    - просматривать рецепты на главной;
    - просматривать страницы пользователей;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;
    - работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов;
    - работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок;
    - подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок;

### администратор

Администратор обладает всеми правами авторизованного пользователя.
<br> Плюс к этому он может:

    - изменять пароль любого пользователя;
    - создавать/блокировать/удалять аккаунты пользователей;
    - редактировать/удалять любые рецепты;
    - добавлять/удалять/редактировать ингредиенты;
    - добавлять/удалять/редактировать теги.

# Админка

В интерфейс админ-зоны выведены следующие поля моделей и фильтры:

### Модели:

    Доступны все модели с возможностью редактирования и удаления записей.

### Модель пользователей:

    Фильтр по email и имени пользователя.

### Модель рецептов:

    В списке рецептов доступны название и авторы рецептов.
    Фильтры по автору, названию рецепта, тегам.
    Выведена информация о популярности рецепта: общее число добавлений этого рецепта в избранное пользователей.

### Модель ингредиентов:

    В списке ингредиентов доступны название ингредиента и единицы измерения.
    Фильтр по названию.

# Ресурсы сервиса

### Рецепт

Рецепт описывается полями:

    Автор публикации (пользователь).
    Название рецепта.
    Картинка рецепта.
    Текстовое описание.
    Ингредиенты: продукты для приготовления блюда по рецепту с указанием количества и единиц измерения.
    Тег.
    Время приготовления в минутах.

### Тег

Тег описывается полями:

    Название.
    Цветовой HEX-код.
    Slug.

### Ингредиент

Ингредиент описывается полями:

    Название.
    Количество (только для рецепта).
    Единицы измерения.

### Список покупок.

Список покупок скачивается в текстовом формате: shopping-list.txt.

## Фильтрация по тегам

При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.
При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. Такой же принцип соблюдается при фильтрации списка избранного.

# Примеры запросов к API.

Запросы к API начинаются с «/api/v1/»

1. регистрация пользователя

POST-запрос: /api/users/
<br /> _Request sample:_

```python
{
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string"
}
```

_Response sample (201):_

```python
{
    "email": "string",
    "id": 0,
    "username": "string",
    "first_name": "string",
    "last_name": "string"
}
```

_Response sample (400):_

```python
{
    «field_name»: [
      «Обязательное поле.»
    ]
}
```

2. Получение токена

POST-запрос: /api/auth/token/login/
<br /> _Request sample:_

```python
{
    «email»: «string»,
    «password»: «string»
}
```

_Response sample (201):_

```python
{
    «token»: «string»
}
```

_Response sample (400):_

```python
{
    «field_name»: [
      «string»
    ]
}
```
