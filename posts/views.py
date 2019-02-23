from django.shortcuts import render
from .models import Post, Tag
from datetime import datetime
from .forms import SubscribeUserForm, ConfirmSubscriberForm
from .utils import send_mail_to
from django.http import HttpResponse
import json


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
        # TODO: Fix counter
        # request.session['counter'] = request.session.get('counter', 0) + 1
        # counter = request.session.get('counter', 0)
        # print(request.session['counter'])
        # if counter == 5:
        #     return HttpResponse(
        #         json.dumps({"error_msg": "You have tried 5 times. Wait for 10 minutes before subscribing"}),
        #         content_type="application/json"
        #     )
        #     request.session['last_freeze'] = datetime.utcnow()
        # if counter > 5 and (datetime.utcnow() - request.session['last_freeze']).minute >= 1:
        #     request.session['counter'] = 0
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
