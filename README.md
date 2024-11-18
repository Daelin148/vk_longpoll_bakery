# VK_LONGPOLL_BAKERY


### Что может этот проект
Проект преставляет собой чат-бота для сообщества ВК. Пользователь может, используя, навигацию просмотреть имеющиеся продукты сообщества


#### Основной стек технологий:
 • vk_api
 • sqlalchemy
 • Docker
 • Redis
 • PostgreSQL
 

### Как развернуть проект:
1. Форкнуть репозиторий в свой Github и клонировать  его:

```
git clone https://github.com/{Username}/api_yamdb
```
2. Добавить следующие secrets в .env своего локального репозитория:
- VK_LONPOLL_API_TOKEN=<YOUR_API_TOKEN>
- POSTGRES_DB=vk_lonpoll_bakery
- POSTGRES_USER=vk_lonpoll_bakery_user
- POSTGRES_PASSWORD=vk_lonpoll_bakery_password
- DB_NAME=vk_lonpoll_bakery
- DB_HOST=postgres
- DB_PORT=5432
- REDIS_HOST=redis
- REDIS_PORT=6379
- REDIS_PASSWORD=my_redis_password
- REDIS_USER=my_user
- REDIS_USER_PASSWORD=my_user_password

3. Для запуска проекта необходимо перейти в корневой каталог и выполнить команду:
```
 docker-compose up -d
```

## Автор проекта:

- Соколов Андрей - https://github.com/Daelin148