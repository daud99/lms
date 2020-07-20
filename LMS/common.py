from LMS.settings import FTP_HOST, FTP_USER, FTP_PASSWORD
import ftplib
import urllib.request as urllib
from pathlib import Path
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
