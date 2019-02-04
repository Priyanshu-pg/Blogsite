from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import Post, Tag
from datetime import datetime
from .forms import SubscribeUserForm, ConfirmSubscriberForm
from .utils import send_mail_to
from smtplib import SMTPException
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse
import json
# Create your views here.


current_email=None

def handle_form(request, form):
    if form.is_valid():
        try:
            send_confirmation_mail(request, form.cleaned_data["email"])
        except SMTPException:
            return HttpResponseRedirect('home')

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
        current_email = request.POST.get('email')
        return send_mail_to(request, current_email)

def confirm_subscriber(request, usermail):
    if request.method == 'POST':
        form = ConfirmSubscriberForm(request.POST)
        if form.is_valid():
            new_subscriber = form.save(commit=False)
            new_subscriber.email = usermail
            new_subscriber.save()
    else:
        form = ConfirmSubscriberForm()
    return render(request, "_confirm_subscription.html", {"form": form})