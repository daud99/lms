from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from event.models import EventCategories, EventImage, Event
from event.forms import LocationForm
from account.models import User
from LMS import common
from datetime import datetime
import json
# Create your views here.

@common.user_is_loggedin_and_is_admin_or_trainer
def addEventCategory(request):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        category_code = request.POST["category_code"]
        category_priority = request.POST["category_priority"]
        category_image = request.FILES["category_image"]
        if "category_status" in request.POST:
            category_status = 1
        else:
            category_status = 0

        try:
            common.uploadImageToFTP(category_image.name, category_image)
            current_user = User.objects.get(email=request.user.email)
            event_category = EventCategories(category_name=category_name, category_code=category_code, category_image_url=category_image.name, category_priority=category_priority, status=category_status, created_user=current_user, updated_user=current_user)
            event_category.save()

        except Exception as e:
            print(e)
            # here will send the user feedback
            messages.error(request, "Make sure Category Name, Code and Priority are UNIQUE!")
            context = {"values": request.POST}
            return render(request, 'event/add_event_category.html', context=context)
        messages.success(request, "Event Category added successfully!")
        return redirect("dashboard:event_categories")
    else:
        return render(request, 'event/add_event_category.html')


def listEventCategories(request):
    event_categories = EventCategories.objects.all()
    for category in event_categories:
        common.downloadImageFromFTP(category.category_image_url)
    context = {"event_categories": event_categories}
    return render(request, "event/event_categories.html", context=context)

@common.user_is_loggedin_and_is_admin_or_trainer
def editEventCategory(request, id):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        category_code = request.POST["category_code"]
        category_priority = request.POST["category_priority"]
        if "category_status" in request.POST:
            category_status = 1
        else:
            category_status = 0

        try:
            current_user = User.objects.get(email=request.user.email)
            if "category_image" in request.FILES:
                category_image = request.FILES["category_image"]
                common.uploadImageToFTP(category_image.name, category_image)
                EventCategories.objects.filter(id=id).update(category_name=category_name, category_code=category_code, category_image_url=category_image.name, category_priority=category_priority, status=category_status, updated_user=current_user)
            else:
                EventCategories.objects.filter(id=id).update(category_name=category_name, category_code=category_code,
                                                         category_priority=category_priority, status=category_status,
                                                         updated_user=current_user)
        except Exception as e:
            print("Exception while updating the event category")
            print(e)
            # here will send the user feedback
            messages.error(request, "Make sure Category Name, Code and Priority are UNIQUE!")
            context = {"values": request.POST}
            return render(request, 'event/edit_event_category.html', context=context)
        messages.success(request, "Event Category updated successfully")
        return redirect("dashboard:event_categories")
    else:
        try:
            event_category = EventCategories.objects.get(id=id)
            context = {"event_category": event_category}
        except Exception as e:
            messages.error(request, "Event Category with such event does not exist!")
            print("Exception while getting EventCategory")
            print(e)
        return render(request, 'event/edit_event_category.html', context=context)


@common.user_is_loggedin_and_is_admin_or_trainer
def deleteEventCategory(request, id):
    try:
        event_category = get_object_or_404(EventCategories, id=id)
        event_category.delete()
        messages.success(request, "Event Category deleted successfully!")
    except Exception as e:
        print("Exception while deleting event category")
        print(e)
        messages.error(request, "Deleting event category is unsuccessful!")
    event_categories = EventCategories.objects.all()
    for category in event_categories:
        common.downloadImageFromFTP(category.category_image_url)
    context = {"event_categories": event_categories}
    return render(request, "event/event_categories.html", context=context)

@common.user_is_loggedin_and_is_admin_or_trainer
def editEvent(request, id):
    if request.method == "POST":
        fields = ["event_name", "event_description", "event_scheduled_status", "event_venue", "event_points",
                  "event_maximum_attende"]
        event_obj = {}
        agenda = []
        agenda_count = 0
        for each in request.POST:
            if each in fields:
                event_obj[each] = request.POST[each]
            else:
                if "session_name" in each:
                    agenda.append({"sessionName": request.POST[each]})
                elif "speaker_name" in each:
                    agenda[agenda_count]["speakerName"] = request.POST[each]
                elif "agenda_start" in each:
                    agenda[agenda_count]["startTime"] = request.POST[each]
                elif "agenda_end" in each:
                    agenda[agenda_count]["endTime"] = request.POST[each]
                elif "venu_name" in each:
                    agenda[agenda_count]["venueName"] = request.POST[each]
                    agenda_count = agenda_count + 1
        start_time = request.POST["start_time"]
        start_date = request.POST["start_date"]
        end_time = request.POST["end_time"]
        end_date = request.POST["end_date"]
        ec = request.POST["event_category"]
        event_location = common.processLocation(request.POST["location"])
        start_date_time = start_date + " " + start_time
        end_date_time = end_date + " " + end_time
        try:
            event_obj["event_start_date"] = datetime.strptime(start_date_time, "%m/%d/%Y %I:%M %p")
        except Exception as e:
            print("Excpetion while parsing date")
            print(e)
            event_obj["event_start_date"] = datetime.strptime(start_date_time, "%m-%d-%Y %I:%M %p")

        try:
            event_obj["event_end_date"] = datetime.strptime(end_date_time, "%m/%d/%Y %I:%M %p")
        except Exception as e:
            print("Excpetion while parsing date")
            print(e)
            event_obj["event_end_date"] = datetime.strptime(end_date_time, "%m-%d-%Y %I:%M %p")

        event_obj["event_agenda"] = json.dumps(agenda)
        if event_location:
            event_obj["event_location"] = event_location
        try:
            event_category = EventCategories.objects.get(category_name=ec)
            current_user = User.objects.get(email=request.user.email)
            event_obj["updated_user"] = current_user
            event_obj["event_category"] = event_category
            try:
                Event.objects.filter(id=id).update(**event_obj)
            except Exception as e:
                print("Exception while updating event")
                print(e)
                messages.error(request, "Make sure event name and venue is UNIQUE!")
                try:
                    form = LocationForm()
                    event = Event.objects.get(id=id)
                    event_categories = EventCategories.objects.all()
                    context = {"event": event, "event_categories": event_categories, 'form': form}
                    return render(request, 'event/edit_event.html', context=context)
                except Exception as e:
                    messages.error(request, "Error!")
                    print("Exception while getting Event for editing")
                    print(e)
                return render(request, "event/events.html")
            events = Event.objects.all()
            if "event_images" in request.FILES:
                for image in request.FILES.getlist("event_images"):
                    try:
                        event = Event.objects.get(id=id)
                        EventImage.objects.filter(event=event).delete()
                        common.uploadImageToFTP(image.name, image)
                        ei = EventImage(event=event, image_url=image.name, created_user=current_user,
                                        updated_user=current_user)
                        ei.save()
                    except Exception as e:
                        print("Exception while saving event image")
                        print(e)
                for event in events:
                    for each in event.event_image_event.all():
                        common.downloadImageFromFTP(str(each))
                context = {"events": events}
                return render(request, "event/events.html", context=context)
        except Exception as e:
            print("Exception while editing event")
            print(e)
            messages.error(request, "Something went wrong while editing")
        context = {"events": events}
        messages.success(request, "Event updated successfully")
        return render(request, "event/events.html", context=context)
    else:
        form = LocationForm()
        try:
            event = Event.objects.get(id=id)
            event_categories = EventCategories.objects.all()
            context = {"event": event, "event_categories": event_categories, 'form': form}
        except Exception as e:
            messages.error(request, "Error!")
            print("Exception while getting Event for editing")
            print(e)
        return render(request, 'event/edit_event.html', context=context)



@common.user_is_loggedin_and_is_admin_or_trainer
def addEvent(request):
    if request.method == "POST":
        fields = ["event_name", "event_description", "event_scheduled_status", "event_venue", "event_points",
                  "event_maximum_attende"]
        event_obj = {}
        agenda = []
        agenda_count = 0
        for each in request.POST:
            if each in fields:
                event_obj[each] = request.POST[each]
            else:
                if "session_name" in each:
                    agenda.append({"sessionName": request.POST[each]})
                elif "speaker_name" in each:
                    agenda[agenda_count]["speakerName"] = request.POST[each]
                elif "agenda_start" in each:
                    agenda[agenda_count]["startTime"] = request.POST[each]
                elif "agenda_end" in each:
                    agenda[agenda_count]["endTime"] = request.POST[each]
                elif "venu_name" in each:
                    agenda[agenda_count]["venueName"] = request.POST[each]
                    agenda_count = agenda_count + 1
        start_time = request.POST["start_time"]
        start_date = request.POST["start_date"]
        end_time = request.POST["end_time"]
        end_date = request.POST["end_date"]
        ec = request.POST["event_category"]
        event_location = common.processLocation(request.POST["location"])
        start_date_time = start_date + " " + start_time
        end_date_time = end_date + " " + end_time
        try:
            event_obj["event_start_date"] = datetime.strptime(start_date_time, "%m/%d/%Y %I:%M %p")
        except Exception as e:
            print("Excpetion while parsing date")
            print(e)
            event_obj["event_start_date"] = datetime.strptime(start_date_time, "%m-%d-%Y %I:%M %p")

        try:
            event_obj["event_end_date"] = datetime.strptime(end_date_time, "%m/%d/%Y %I:%M %p")
        except Exception as e:
            print("Excpetion while parsing date")
            print(e)
            event_obj["event_end_date"] = datetime.strptime(end_date_time, "%m-%d-%Y %I:%M %p")

        event_obj["event_agenda"] = json.dumps(agenda)
        event_obj["event_location"] = event_location
        try:
            event_category = EventCategories.objects.get(category_name=ec)
            current_user = User.objects.get(email=request.user.email)
            event_obj["created_user"] = current_user
            event_obj["updated_user"] = current_user
            event_obj["event_category"] = event_category
            try:
                event = Event(**event_obj)
                event.save()
            except Exception as e:
                print("Exception while saving event")
                print(e)
                messages.error(request, "Make sure event name and venue is UNIQUE!")
                event_categories = EventCategories.objects.all()
                context = {"event_categories": event_categories, "values": request.POST}
                return render(request, "event/add_event.html", context=context)
            if "event_images" in request.FILES:
                for image in request.FILES.getlist("event_images"):
                    common.uploadImageToFTP(image.name, image)
                    try:
                        ei = EventImage(event=event, image_url=image.name, created_user=current_user, updated_user=current_user)
                        ei.save()
                    except Exception as e:
                        print("Exception while saving event image")
                        print(e)
                events = Event.objects.all()
                for event in events:
                    for each in event.event_image_event.all():
                        common.downloadImageFromFTP(str(each))
                context = {"events": events}
                return render(request, "event/events.html", context=context)
        except Exception as e:
            print("Exception while saving event")
            print(e)
        return render(request, "event/events.html")
    else:
        form = LocationForm()
        event_categories = EventCategories.objects.all()
        context = {"event_categories": event_categories, 'form': form}
        return render(request, "event/add_event.html", context=context)

@login_required(login_url="login")
def listEvent(request):
    events = Event.objects.all()
    for event in events:
        for each in event.event_image_event.all():
            common.downloadImageFromFTP(str(each))
    context = {"events": events}
    return render(request, "event/events.html", context=context)

@login_required(login_url="login")
def detailEvent(request, id):
    try:
        # print("Id is ", id)
        event = Event.objects.get(id=id)
        # print(event)
        for each in event.event_image_event.all():
            common.downloadImageFromFTP(str(each))
        context = {"event": event}
        return render(request, "event/event_detail.html", context=context)
    except Exception as e:
        print("Exception while finding the specific event")
        print(e)
        messages.error(request, "event with given ID not found!")
        return render(request, "event/events.html")

@common.user_is_loggedin_and_is_admin_or_trainer
def deleteEvent(request, id):
    try:
        event = get_object_or_404(Event, id=id)
        event.delete()
        messages.success(request, "Event deleted successfully")
    except Exception as e:
        print("Exception while deleting event")
        print(e)
        messages.error(request, "Unable to delete the Event!")
    events = Event.objects.all()
    for event in events:
        for each in event.event_image_event.all():
            common.downloadImageFromFTP(str(each))
    context = {"events": events}
    return render(request, "event/events.html", context=context)