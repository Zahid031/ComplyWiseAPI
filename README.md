## git clone

git clone https://github.com/syful-islam/ComplyWiseApi.git

git remote add origin https://github.com/syful-islam/ComplyWiseApi.git

## run application

~/projects/python$ source djvenv/bin/activate
cd ComplyWiseApi/

python3 manage.py runserver 8080

## Migration script

python3 manage.py makemigrations

## in production

python3 manage.py migrate

## in production for swagger

python3 manage.py collectstatic

## Batch Command to update in github

git add .
git commit -m "Views Updated"
git push origin main

## Command to pull to production from github

git pull origin main

sudo systemctl restart nginx
sudo supervisorctl restart all

os user pass: qazwsx!@#

## view the Swagger or ReDoc documentation

http://127.0.0.1:8000/swagger/ or
http://127.0.0.1:8000/redoc/

## re-publish to production

sudo -u postgres psql

DROP DATABASE complywise;
CREATE DATABASE complywise;

git stash
git pull origin main

python3 manage.py migrate

sudo rm -r staticfiles/
python3 manage.py collectstatic

sudo systemctl restart complywiseapi
