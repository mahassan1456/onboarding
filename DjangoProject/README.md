1. Go to Document root @ "/Code" and type the BASH command pipenv install will automatically install all libraries and dependencies for the project.

2. Database must do initial Migration. Go to root folder at /DjangoProject "python manage.py makemigrations" and then "python manage.py" migrate. The database should now be synced with the application. If you are in the incorrect directory check to make sure the current working directory contains the "manage.py" file. This is the entry point for everything.

---------------------------------------------------------CREATING SUPERUSER-----------------------------------------------------------------
After the databases are migrated you can issue the command in the same directory as "manage.py". "python manage.py createsuperuser" and then follow the prompts for username, and email, and password setup.
--------------------------------------------------------------------------------------------------------------------------------------------

3. Locate the settings.py file located at Code/DjangoProject/mysite/settings.py and find the following Python_Dictionary 

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'HOST': DB_HOST,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'PORT': '3306'
    }
}
4. Set environment variables for each of the variable values above( or hardcode them if you prefer :)  )

5. The file entrypoint for configuring the WSGI server which will communicate with apache/nginx is located at "Code/DjangoProject/mysite/wsgi.py"

6. python manage.py runserver will run the program locally in debug Mode.


