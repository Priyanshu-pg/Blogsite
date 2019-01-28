from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Tag
from datetime import datetime
from .forms import SubscribeUserForm
from .utils import send_confirmation_mail
from smtplib import SMTPException
# Create your views here.

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
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['receiver@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)
        # return handle_form(request, form)
    else:
        form = SubscribeUserForm()
    return render(request, "post_detail.html", {"post": post, "form": form})
