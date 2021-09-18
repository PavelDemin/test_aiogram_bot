## ТЕСТОВЫЙ AIOGRAM БОТ

### Основной функционал
- Регистрация пользователя с запросом имени и номера телефона.
- Запись пользователя на выбраную дату
- Админитратор может принять заявку или отклонить с уведомлением причины отклонения

### Используемые библиотеки:
- aiogram "2.14.3"
- gino "1.0.1"
- loguru "0.5.3"
- pydantic "1.8.2"

### Инструкци по установке:
- Клонировать текущий репозиторий <code> git clone https://github.com/PavelDemin/test_aiogram_bot.git </code>
- В <code> docker-compose.yml </code> необходимо изменить <b> TELEGRAM_TOKEN </b> и <b> DOMAIN </b> на свои.
- При необходимости изменить путь до SSL сертификата вашего домена <code> /etc/letsencrypt/:/etc/letsencrypt/ </code>
- Задать Telegram ID администратора в <b> ADMIN </b>

### Запуск

- <code> docker-compose up -d </code>