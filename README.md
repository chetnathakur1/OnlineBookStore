Create a virtual environment:
pyhton -m venv .venv

Then, activate your virtual environment:
For Linux - source .venv/bin/activate 

Now install the requirement.txt file:
pip install -r requirement.txt

Set up the database:
python manage.py makemigrations
python manage.py migrate

Create super user(admin):
python manage.py createsuperuser

Now run the server:
python manage.py runserver
