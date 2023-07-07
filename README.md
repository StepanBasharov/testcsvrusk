API DOCUMENTATION

SETUP

unzip csv_reade.zip<br>
cd csv_reader<br>
docker-compose up 

ENDPOINTS

/api/upload/ - загрузка CSV файла формата (customer, item, total, quantity, date)<br>
/api/top/ - получение 5 пользователей потративших максимальную сумму

Приложение основано на DRF, использует многопоточный сервер wsgi сервер gunicorn, запускается командой docker-compose up