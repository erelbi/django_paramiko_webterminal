# [Django Paramiko Web Terminal](https://deney.site)
![](github.gif)
** Web Tabanlı Django Terminal

```bash
$ # Get the code
$ git clone https://github.com/erelbi/django_paramiko_webterminal.git
$ cd django_paramiko_webterminal
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$ 
$ # Install modules
$ # SQLIte version
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

<br />

## Read Me

For this project Expert Systems course, see.
With SSH, we can send commands to remote clients and see the result. It has an expert system that analyzes the scenario for script writing.
