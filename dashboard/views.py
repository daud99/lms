from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from LMS import common
import os
# Create your views here.

@login_required(login_url='account_login')
def index(request):
    image_name = request.user.image_url
    common.downloadImageFromFTP(image_name)
    final_img_path = os.path.join('img', image_name)
    context = {"img": final_img_path}
    return render(request, 'dashboard/index.html', context=context)

