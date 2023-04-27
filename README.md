# Website "Grocery assistant"

## About the author

Tankhaev Danzan

Python developer

Email: dtankhaev@gmail.com

Telegram: @dtankhaev

## Technology stack

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

## Description

"Grocery Assistant"
The site is a database of culinary recipes. Users can create their own recipes, read recipes of other users, subscribe to interesting authors, add the best recipes to favorites, as well as create a shopping list and upload it in THT format. There is also a docker-compose file that allows you to quickly deploy a database container (PostgreSQL), a django + gunicorn project container and an nginx container.

API documentation is available to [here](http://51.250.20.19//api/docs /)

## Preparation and launch of the project

### Clone the repository to the local machine:

```
git clone git@github.com:dtankhaev/foodgram-project-react.git
``

## To work with a remote server (on ubuntu):

- Log in to your remote server

- Install docker on the server:

``
installing sudo apt docker.io
``

- Install docker-create on the server:

``
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose -$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- Locally edit the infra/nginx.conf file and enter your IP in the server_name line
- Copy the docker-compose files.yml and nginx.conf from the infra directory to the server:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

- create .env file and enter:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<postgres database name>
DB_USER=<db user>
DB_PASSWORD=<password>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<django project secret key>
```
- To work with Workflow, add environment variables to GitHub Secrets for work:

```
DOCKER_PASSWORD=<DockerHub password>
DOCKER_USERNAME=<username>

SECRET_KEY=<django project secret key>

USER=<username to connect to the server>
HOST=<Server IP>
PASSPHRASE=<password for the server, if installed>
SSH_KEY=<your SSH key (to get the command: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID of the chat to which the message will be sent>
TELEGRAM_TOKEN=<your bot's token>
```

It consists of a three-step workflow:

- Checking the code for compliance with PEP8
- Assembling and publishing the backend image on DockerHub.
- Automatic deployment to a remote server using migrations and static assembly
- Sending notifications to the telegram chat.

- Build docker on the server-create:

```
sudo docker-compose up -d --build
```

- After a successful build on the server, run the commands (only after the first deployment):
- Create a Django superuser:
``
sudo docker -creates an exec server part for python management.py creates a superuser
``
- The project will be available via your IP

## Registration and authorization

The service provides a system of registration and authorization of users.
Required fields for the user:

<li> Login
<li> Password
<li> Email
<li> Name
<li> Surname

## Access rights to the service resources

### unauthorized users can:

- create an account;
- view recipes on the home page;
- view individual recipe pages;
- filter recipes by tags;

### authorized users can:

- log in with your username and password;
- log out (log out);
- change your password;
- create/edit/delete your own recipes;
- view recipes on the home page;
- view user pages;
- view individual recipe pages;
- filter recipes by tags;
- work with a personal favorites list: add recipes to it or delete them, view your favorite recipes page;
- work with a personal shopping list: add/remove any recipes, upload a file with the number of necessary ingredients for recipes from the shopping list;
- subscribe to recipe authors' publications and cancel subscriptions, view your subscriptions page;

### administrator

The administrator has all the rights of an authorized user.
<br> Plus it can:

- change the password of any user;
- create/block/delete user accounts;
- edit/delete any recipes;
- add/remove/edit ingredients;
- add/remove/edit tags.

# Admin panel

The following model fields and filters are displayed in the admin zone interface:

### Models:

All models are available with the ability to edit and delete records.

### User Model:

Filter by username and email.

### Recipe Model:

The name and authors of the recipes are available in the recipe list.
Filters by author, recipe name, tags.
Information about the popularity of the recipe is displayed: the total number of additions of this recipe to the favorites of users.

### Ingredients Model:

The ingredient name and units of measurement are available in the list of ingredients.
Filter by name.

# Service Resources

### Recipe

The recipe is described by the fields:

The author of the publication (user).
The name of the recipe.
Picture of the recipe.
Text description.
Ingredients: products for cooking according to a recipe with an indication of the quantity and units of measurement.
Tag.
Cooking time in minutes.

### Tag

The tag is described by fields:

Title.
Color HEXADECIMAL code.
Slug.

### Ingredient

The ingredient is described by the fields:

Title.
Quantity (for prescription only).
Units of measurement.

### Shopping list.

The Shopping list is downloaded in text format: shopping-list.txt .

## Filtering by tags

Clicking on the tag name displays a list of recipes marked with this tag. Filtering can be carried out by several tags in a combination of "or": if several tags are selected, recipes that are marked with at least one of these tags should be shown as a result.
When filtering on the user's page, only the recipes of the selected user are filtered. The same principle is observed when filtering the favorites list.

# Examples of API requests.

API requests start with "/api/v1/"

1. user registration

POST request: /api/users/
<br /> _Request sample:_

`python
{
"email": "string",
"username": "string",
"first_name": "string",
"last_name": "string",
"password": "string"
}
``

_ Sample response (201):_

`python
{
"email": "string",
"id": 0,
"username": "string",
"first_name": "string",
"last_name": "string"
}
``

_ Sample response (400):_

`python
{
"field_name": [
"Required field."
]
}
```

2. Getting a token

POST request: /api/auth/token/login/
<br/> _Request sample:_

`python
{
"email": "string",
"password": "string"
}
``

_ Sample response (201):_

`python
{
"token": "string"
}
``

_ Sample response (400):_

`python
{
"field_name": [
"string"
]
}
```
