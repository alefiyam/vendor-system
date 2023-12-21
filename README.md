# vendor-management-system
To configure this appliction into your local machine,follow these instructions

Install python version 3.11

Make virtual environment with python 3.11
virtualenv vendor_env -p python3.11

Activate virtual environment

Take clone in your local machine.
git clone https://github.com/alefiyam/vendor-system.git

Then navigate to vendor-system directory and execute the following commands

pip install -r requirements.txt
this will install all require application dependencies.

Run migrations to create tables in database.
python manage.py makemigrations
python manage.py migrate

To start this application just run the following command
python manage.py runserver