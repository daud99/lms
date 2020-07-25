from django.shortcuts import redirect
from django.contrib import messages
from LMS.settings import FTP_HOST, FTP_USER, FTP_PASSWORD, GEOCODE_URL
import ftplib
import urllib.request as urllib
from pathlib import Path
import requests
import os

def uploadImageToFTP(image_name, image):
    try:
        session = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASSWORD)
        session.storbinary(f'STOR {image_name}', image)
        session.quit()
    except Exception as e:
        print("Exception while uploading image to FTP Server")
        print(e)

def downloadImageFromFTP(image_name):
    ftp_url = f'ftp://{FTP_USER}:{FTP_PASSWORD}@{FTP_HOST}'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = os.path.join(BASE_DIR, "static", "img", image_name)
    my_file = Path(IMG_DIR)
    try:
        if not my_file.exists():
            img = urllib.urlopen(f"{ftp_url}/{image_name}")
            with open(IMG_DIR, 'wb') as file:
                file.write(img.read())
    except Exception as e:
        print("Exception while downloading image from FTP Server")
        print(e)

def user_is_loggedin_and_is_admin_or_trainer(func):
    def wrapper(*args, id="default"):
        if not args[0].user.is_authenticated:
            messages.error(args[0], 'You are not Logged In')
            return redirect('account_login')
        elif not (args[0].user.role.role_name in ["admin", "trainer"]):
            messages.error(args[0], 'Only admin and trainer can access this route')
            return redirect('dashboard:index')
        else:
            if not(id == "default"):
                return func(args[0], id)
            else:
                return func(args[0])
    return wrapper

def processLocation(location):
    if location:
        event_location = {"type": "Point"}
        event_location["coordinates"] = location.split(",")
        return event_location
    else:
        return {}

def getLocationFromLangLat(location):

    location_name = "Not found"
    try:
        if location:
            if "coordinates" in location:
                lat = location["coordinates"][0]
                log = location["coordinates"][1]
                final_location = lat+","+log
                final_url = GEOCODE_URL+final_location+"?json=1"
                # print("final_url", final_url)
                res = requests.get(final_url)
                res = res.json()
                if "osmtags" in res:
                    location_name = res["osmtags"]
                    if "name" in location_name:
                        location_name = location_name["name"]
                    elif "city" in location_name:
                        location_name = location_name["city"]
                    else:
                        location_name = "Not found"
            else:
                location_name = "Not found"
        else:
            location_name = "Not found"
    except Exception as e:
        print("Exception while finding location form longitude and latitude")
        print(e)

    return  location_name

def getLangLat(location):
    if location:
        if "coordinates" in location:
            lat = location["coordinates"][0]
            log = location["coordinates"][1]
            final_location = lat+","+log
        return final_location
    else:
        ""
