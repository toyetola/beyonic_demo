Create a virtual environment to run your Django application:

In your terminal, run:

```python -m venv env```

The above would create a folder named ```env``` Then, you can go ahead to activate the environment with the following command in your terminal:

Linux and Mac:

```source env/bin/activate```

Windows:

```env\Scripts\activate```

Clone your app here and install dependencies

```pip -r install requirements.txt```

Create a ```.env``` file and copy the content of ```.env.dist``` to it

Edit ```.env```appropriately according to your local computer DB set up and you can put any random string as secret key or generate it from your app.

Run your app

```python manage.py runserver```

Test out the urls on this document:

https://documenter.getpostman.com/view/3707157/VUr1FCEc