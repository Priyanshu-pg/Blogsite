from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from datetime import datetime
# Create your views here.

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

def post_detail(request, year, month, slug):
    post = Post.objects.get(slug=slug)
    print(post)
    return render(request, "post_detail.html", {"post": post})
