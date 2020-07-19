from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from LMS.settings import FTP_HOST, FTP_PASSWORD, FTP_USER
import urllib.request as urllib
from pathlib import Path
import os
# Create your views here.

@login_required(login_url='login')
def index(request):
    image_name = request.user.image_url
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
        print(e)

    final_img_path = os.path.join('img', image_name)
    context = {"img": final_img_path}
    return render(request, 'dashboard/index.html', context=context)