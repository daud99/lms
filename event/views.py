from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from event.models import EventCategories, EventImage, Event
from account.models import User
from LMS import common
from datetime import datetime
# Create your views here.

@login_required(login_url='login')
def addEventCategory(request):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        category_code = request.POST["category_code"]
        category_periorty = request.POST["category_perority"]
        category_image = request.FILES["category_image"]
        category_status = request.POST["category_status"]

        try:
            common.uploadImageToFTP(category_image.name, category_image)
            current_user = User.objects.get(email=request.user.email)
            event_category = EventCategories(category_name=category_name, category_code=category_code, category_image_url=category_image.name, category_priority=category_periorty, status=category_status, created_user=current_user, updated_user=current_user)
            event_category.save()

        except Exception as e:
            print(e)

        return redirect("dashboard:event_categories")
    else:
        return render(request, 'event/add_event_category.html')


def listEventCategories(request):
    event_categories = EventCategories.objects.all()
    for category in event_categories:
        common.downloadImageFromFTP(category.category_image_url)
    context = {"event_categories": event_categories}
    return render(request, "event/event_categories.html", context=context)

@login_required(login_url='login')
def editEventCategory(request, id):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        category_code = request.POST["category_code"]
        category_periorty = request.POST["category_perority"]
        category_status = request.POST["category_status"]

        try:
            current_user = User.objects.get(email=request.user.email)
            if "category_image" in request.FILES:
                category_image = request.FILES["category_image"]
                common.uploadImageToFTP(category_image.name, category_image)
                EventCategories.objects.filter(id=id).update(category_name=category_name, category_code=category_code, category_image_url=category_image.name, category_priority=category_periorty, status=category_status, updated_user=current_user)
            else:
                EventCategories.objects.filter(id=id).update(category_name=category_name, category_code=category_code,
                                                         category_priority=category_periorty, status=category_status,
                                                         updated_user=current_user)
        except Exception as e:
            print("Exception while updating the event category")
            print(e)

        return redirect("dashboard:event_categories")
    else:
        try:
            event_category = EventCategories.objects.get(id=id)
            context = {"event_category": event_category}
        except Exception as e:
            print("Exception while getting EventCategory")
            print(e)
        return render(request, 'event/edit_event_category.html', context=context)


@login_required(login_url="login")
def deleteEventCategory(request, id):
    try:
        event_category = get_object_or_404(EventCategories, id=id)
        event_category.delete()
    except Exception as e:
        print("Exception while deleting event category")
        print(e)
    event_categories = EventCategories.objects.all()
    for category in event_categories:
        common.downloadImageFromFTP(category.category_image_url)
    context = {"event_categories": event_categories}
    return render(request, "event/event_categories.html", context=context)


@login_required(login_url="login")
def addEvent(request):
    if request.method == "POST":
        event_category = request.POST["event_category"]
        event_name = request.POST["event_name"]
        event_description = request.POST["event_description"]
        status = request.POST["status"]
        start_time = request.POST["start_time"]
        start_date = request.POST["start_date"]
        end_time = request.POST["end_time"]
        end_date = request.POST["end_date"]
        event_venue = request.POST["event_venue"]
        event_points = request.POST["event_points"]
        event_capacity = request.POST["event_capacity"]
        current_user = User.objects.get(email=request.user.email)
        start_date_time = start_date+" "+start_time
        end_date_time = end_date+" "+end_time
        start_date_time = datetime.strptime(start_date_time, "%m-%d-%Y %I:%M %p")
        end_date_time = datetime.strptime(end_date_time, "%m-%d-%Y %I:%M %p")
        try:
            ec = EventCategories.objects.get(category_name=event_category)
            event = Event(event_category=ec, event_name=event_name, event_description=event_description, event_scheduled_status=status, event_venue=event_venue, event_start_date=start_date_time, event_end_date=end_date_time, event_points=event_points, event_maximum_attende=event_capacity, created_user=current_user, updated_user=current_user)
            event.save()
            if "event_images" in request.FILES:
                for image in request.FILES.getlist("event_images"):
                    common.uploadImageToFTP(image.name, image)
                    try:
                        ei = EventImage(event=event, image_url=image.name, created_user=current_user, updated_user=current_user)
                        ei.save()
                    except Exception as e:
                        print("Exception while saving event image")
                        print(e)
                return redirect("login")
            else:
                print("no it is not in Files")
                return redirect("signup")
        except Exception as e:
            print("Exception while saving event")
            print(e)


    else:
        event_categories = EventCategories.objects.all()
        context = {"event_categories": event_categories}
        return render(request, "event/add_event.html", context=context)