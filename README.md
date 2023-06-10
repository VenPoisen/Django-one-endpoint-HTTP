# Django-one-endpoint-HTTP
Caso práctico donde el endpoint devuelve el estado y tiempo de respuesta de un dominio o ip proporcionado

## Test locally
- Clone git
```git clone https://github.com/VenPoisen/Django-one-endpoint-HTTP.git```
- Create a virtual environment venv and activate it 
- Create .env file based on .env-example
- Install requirements.txt ```pip install -r requirements.txt```
- Migrate and runserver 
```
python manage.py migrate
python manage.py runserver
```

## Usage 
- Using Postman/Insomnia or cURL, pass a querystring parameter called "dominio" and an optional parameter called "ip"
Example ```curl -v -G "http://127.0.0.1:8000/?dominio=www.stackoverflow.com&ip=151.101.1.69"```
