from django.shortcuts import render
from .models import Post, Tag
from datetime import datetime
from .forms import SubscribeUserForm, ConfirmSubscriberForm
from .utils import send_mail_to
from django.http import HttpResponse
import json
import math


def home(request):
    post_list = Post.objects.order_by('create_time')
    return render(request, "index.html", {"post_list": post_list})


def year_archive(request, year):
    post_list = Post.objects.filter(create_time__year=year).order_by('create_time')
    return render(request, "year_archive.html", {"post_list": post_list, "year": year})


def month_archive(request, year, month):
    print(type(month))
    monthinteger = int(month)
    print(monthinteger)
    monthName = datetime.date(1900, monthinteger, 1).strftime('%B')
    print(monthName)
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
    return render(request, "month_archive.html", {"post_list": post_list, "month": month})


def tag_archive(request, tag):
    # TODO: Check if this tag exists or not
    post_list = Post.objects.filter(tags__tag_name=tag)
    return render(request, "tag_archive.html", {"post_list": post_list, "tag": tag})


def post_detail(request, year, month, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = SubscribeUserForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SubscribeUserForm()
    return render(request, "post_detail.html", {"post": post, "form": form})


def send_confirmation_mail(request):
    if request.method == 'POST':
        max_resend_count = 5
        resend_waiting_time = 10
        counter = request.session.get('counter', 0)
        counter += 1
        request.session['counter'] = counter

        if counter == max_resend_count:
            request.session['last_freeze'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
            return HttpResponse(
                json.dumps({"error_msg": "You have tried {0} times. "
                            "Wait for {1} minutes before trying again.".format(max_resend_count, resend_waiting_time)}),
                content_type="application/json"
            )

        if counter > max_resend_count:
            time_spent_in_seconds = (datetime.utcnow() -
                                     datetime.strptime(request.session.get('last_freeze',
                                                                           datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")),
                                                        "%Y-%m-%d %H:%M:%S.%f")
                                     ).seconds
            if time_spent_in_seconds >= 60*resend_waiting_time:
                request.session['counter'] = 0
                counter = 0
            else:
                minutes_left = max(0, math.ceil((60*resend_waiting_time - time_spent_in_seconds)/60))
                return HttpResponse(
                    json.dumps({"error_msg": "You have tried more than {0} times. "
                                "Wait for {1} minutes before trying again".format(max_resend_count, minutes_left)}),
                    content_type="application/json"
                )

        if counter <= max_resend_count:
            current_email = request.POST.get('email')
            return send_mail_to(request, current_email)

    else:
        form = SubscribeUserForm()
        return render(request, "_subscribe_form.html", {"form": form})


def confirm_subscriber(request, user_mail):
    if request.method == 'POST':
        form = ConfirmSubscriberForm(request.POST)
        if form.is_valid():
            new_subscriber = form.save(commit=False)
            new_subscriber.email = user_mail
            new_subscriber.save()
            form.save_m2m()  # saving many-to-many relationship as side effect of commit=false
    else:
        form = ConfirmSubscriberForm()
    return render(request, "_confirm_subscription.html", {"form": form})
from django.shortcuts import render
from .models import Post, Tag
from datetime import datetime
from .forms import SubscribeUserForm, ConfirmSubscriberForm
from .utils import send_mail_to
from django.http import HttpResponse
import json
import math


def home(request):
    post_list = Post.objects.order_by('create_time')
    return render(request, "index.html", {"post_list": post_list})


def year_archive(request, year):
    post_list = Post.objects.filter(create_time__year=year).order_by('create_time')
    return render(request, "year_archive.html", {"post_list": post_list, "year": year})


def month_archive(request, year, month):
    print(type(month))
    monthinteger = int(month)
    print(monthinteger)
    monthName = datetime.date(1900, monthinteger, 1).strftime('%B')
    print(monthName)
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
    return render(request, "month_archive.html", {"post_list": post_list, "month": month})


def tag_archive(request, tag):
    # TODO: Check if this tag exists or not
    post_list = Post.objects.filter(tags__tag_name=tag)
    return render(request, "tag_archive.html", {"post_list": post_list, "tag": tag})


def post_detail(request, year, month, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = SubscribeUserForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SubscribeUserForm()
    return render(request, "post_detail.html", {"post": post, "form": form})


def send_confirmation_mail(request):
    if request.method == 'POST':
        counter = request.session.get('counter', 0)
        counter += 1
        request.session['counter'] = counter
        print(request.session['counter'])

        if counter == 5:
            request.session['last_freeze'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
            return HttpResponse(
                json.dumps({"error_msg": "You have tried 5 times. "
                                         "Wait for 10 minutes before trying again."}),
                content_type="application/json"
            )
        if counter > 5:
            time_spent_in_seconds = (datetime.utcnow() -
                                     datetime.strptime(request.session.get('last_freeze',
                                                                           datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")),
                                                       "%Y-%m-%d %H:%M:%S.%f"
                                                       )
                                     ).seconds
            if time_spent_in_seconds >= 600:
                request.session['counter'] = 0
            minutes_left = max(0, math.ceil((600 - time_spent_in_seconds)/60))
            return HttpResponse(
                json.dumps({"error_msg": "You have tried more than 5 times. "
                                         "Wait for {0} minutes before trying again".format(minutes_left)}),
                content_type="application/json"
            )

        if counter <= 5:
            current_email = request.POST.get('email')
            return send_mail_to(request, current_email)
    else:
        form = SubscribeUserForm()
        return render(request, "_subscribe_form.html", {"form": form})


def confirm_subscriber(request, user_mail):
    if request.method == 'POST':
        form = ConfirmSubscriberForm(request.POST)
        if form.is_valid():
            new_subscriber = form.save(commit=False)
            new_subscriber.email = user_mail
            new_subscriber.save()
            form.save_m2m()  # saving many-to-many relationship as side effect of commit=false
    else:
        form = ConfirmSubscriberForm()
    return render(request, "_confirm_subscription.html", {"form": form})
