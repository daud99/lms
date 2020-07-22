# LMS

## Setting UP Environment

1. Install dependency for creating virtual environment

```
pip install virtualenv
```

2. Create virtual environment

```
virtualenv myprojectenv
```

3. Activating the virtual environment for Linux

```
source venv/bin/activate
```

For window

```
.\venv\bin\activate
```

## Installing Dependencies

1. Open terminal. Make sure to be at the root of your project

```
pip install -r requirements.txt
```

2. Make sure MongoDB server is install.

## Setting UP Database

1. Open your console and run this command 		

```
mongo
```

2. Creating DB

```
user database_name
```

3. Setting up credentials for DB

   ```
   db.createUser(
      {
        user: "username",
        pwd: "password",
        roles: [ "userAdmin" ]
      }
   )
   ```

4. Make changes in LMS/settings.py file for DB respectively

   ```
   DATABASES = {
       'default': {
           'ENGINE': 'djongo',
           'ENFORCE_SCHEMA': False,
           'NAME': 'lms',
           'HOST': 'mongodb://localhost:27017/lms',
           'PORT': 27017,
           'USER': 'daud',
           'PASSWORD': 'daud123'
       }
   }
   ```

5. run these commands

```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

6. Create super user by providing the required information

```
python manage.py createsuperuser
```

7. Login at

   ```
   http://127.0.0.1:8000/admin
   ```

## Configuring project

1. Make sure to make changes accordingly in **LMS/settings.py**

   ```
   
   # FTP SERVER
   
   FTP_HOST = 'tms.itcomlive.com'
   FTP_USER = 'eventimages'
   FTP_PASSWORD = 'yn71%3Nv'
   
   # SMTP SERVER
   
   EMAIL_USE_TLS = True
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_HOST_USER = 'thedarkbot9@gmail.com'
   EMAIL_HOST_PASSWORD = 'password'
   EMAIL_PORT = 587
   DEFAULT_FROM_EMAIL = 'Roche Team <admin@roche.com>'
   
   # Key for map
   MAPBOX_KEY = "pk.eyJ1IjoiZGF1ZGFobWVkIiwiYSI6ImNrY3gzNG10ZDBrN3kydHJwc3lzd20yeTIifQ.cx574AlQZYO-AvIrR_57Aw"
   
   # GEO CODING
   GEOCODE_URL = "https://geocode.xyz/"
   ```

## Restrictions

> Right now, the GEO coding API is use for mapping longitude and latitude to **Location** but it's limited to one request per second more over. It's free so is it slow. You can switch to google API.

## Future Support

Contact me at **daud.ahmed@tranchulas.com.**

