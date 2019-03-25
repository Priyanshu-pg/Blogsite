from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from posts.models import Post, Tag
from posts.models import UserMailIdMap
from posts.models import SubscribedUsers
from datetime import datetime
from posts.forms import *
from posts.utils import send_mail_to
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib import messages
import json
import math
from django.contrib.auth.hashers import make_password, check_password


#TODO: Check time zone issues with mysql table


def home(request):
    post_list = Post.objects.order_by('create_time')
    if len(post_list) == 0:
        raise Http404("No posts found!")
    return render(request, "index.html", {"post_list": post_list})


def year_archive(request, year):
    post_list = Post.objects.filter(create_time__year=year).order_by('create_time')
    if len(post_list) == 0:
        raise Http404("No posts found for the year.")
    return render(request, "year_archive.html", {"post_list": post_list, "year": year})


def month_archive(request, year, month):
    month_name = datetime(1900, int(month), 1).strftime('%B')
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
    if len(post_list) == 0:
        raise Http404("No posts found for the month.")
    return render(request, "month_archive.html", {"post_list": post_list, "month": month_name})


def tag_archive(request, tag):
    post_list = Post.objects.filter(tags__tag_name=tag)
    if len(post_list) == 0:
        raise Http404("No posts found for the tag.")
    return render(request, "tag_archive.html", {"post_list": post_list, "tag": tag})


def post_detail(request, year, month, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = SubscribeUserForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SubscribeUserForm()
    return render(request, "post_detail.html", {"post": post, "form": form})


def freeze_submission(request, max_resend_count, resend_waiting_time):
    request.session['last_freeze'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    return HttpResponse(
        json.dumps({"error_msg": "You have tried {0} times. "
                                 "Wait for {1} minutes before trying again.".format(max_resend_count,
                                                                                    resend_waiting_time)}),
        content_type="application/json"
    )


def calc_time_spent_in_seconds(request):
    last_freeze_time = request.session.get('last_freeze', datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"))
    time_spent_in_seconds = (datetime.utcnow() -
                             datetime.strptime(last_freeze_time, "%Y-%m-%d %H:%M:%S.%f")
                             ).seconds
    return time_spent_in_seconds


def get_user_mail_and_hash(request):
    current_email = request.POST.get('email')
    try:
        user_mail_id_map = UserMailIdMap.objects.get(email=current_email)
    except UserMailIdMap.DoesNotExist:
        user_mail_id_map = UserMailIdMap(email=current_email)
        user_mail_id_map.save()
    return user_mail_id_map.email, user_mail_id_map.email_hash


def send_confirmation_mail(request):
    if request.method == 'POST':
        max_resend_count = 5
        resend_waiting_time = 10

        counter = request.session.get('counter', 0)
        counter += 1
        request.session['counter'] = counter

        if counter == max_resend_count:
            return freeze_submission(request)

        if counter > max_resend_count:
            time_left_to_unfreeze = 60*resend_waiting_time - calc_time_spent_in_seconds(request)
            if time_left_to_unfreeze <= 0:
                request.session['counter'] = 0
                counter = 0
            else:
                minutes_left = max(0, math.ceil(time_left_to_unfreeze/60))
                return HttpResponse(
                    json.dumps({"error_msg": "You have tried more than {0} times. "
                                "Wait for {1} minutes before trying again".format(max_resend_count, minutes_left)}),
                    content_type="application/json"
                )

        if counter <= max_resend_count:
            current_email, current_email_hash = get_user_mail_and_hash(request)
            return send_mail_to(request, current_email, current_email_hash)

    else:
        form = SubscribeUserForm()
        return render(request, "_subscribe_form.html", {"form": form})


def get_user_mail_obj(user_mail_hash):
    try:
        user_mail_obj = UserMailIdMap.objects.get(email_hash=user_mail_hash)
        return user_mail_obj
    except UserMailIdMap.DoesNotExist:
        raise Http404("No user email is registered. Please register again")


def get_existing_subscription(user_mail):
    try:
        old_subscriber = SubscribedUsers.objects.get(email=user_mail)
        return old_subscriber
    except SubscribedUsers.DoesNotExist:
        return None


def update_subscription(request, subscriber, form):
    tags_followed = Tag.objects.filter(tag_name__in=form.cleaned_data["tags_followed"])
    subscriber.frequency = form.cleaned_data["frequency"]
    subscriber.tags_followed.set(tags_followed)
    subscriber.save()
    messages.success(request, 'Your subscription plan has been updated')


def unsubscribe(request, user_mail_hash):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            if 'yes' in request.POST:
                user_mail_obj = get_user_mail_obj(user_mail_hash)
                subscriber = get_existing_subscription(user_mail_obj.email)
                if subscriber is None:
                    messages.success(request, 'You have not subscribed yet.')
                else:
                    subscriber.delete()
                    messages.success(request, "Unsubscribed")
            if 'no' in request.POST:
                messages.success(request, "Still subscribed")
    else:
        form = UnsubscribeForm()
    return render(request, "unsubscribe.html", {"form": form})


def modify_subscription(request, user_mail_hash):
    if request.method == 'POST':
        form = SubscriptionChoiceForm(request.POST)
        if form.is_valid():
            user_mail_obj = get_user_mail_obj(user_mail_hash)
            subscriber = get_existing_subscription(user_mail_obj.email)
            if subscriber is None:
                messages.success(request, 'You have not subscribed yet.')
            else:
                update_subscription(request, subscriber, form)
    else:
        form = SubscriptionChoiceForm()
    return render(request, "_confirm_subscription.html", {"form": form})


def confirm_subscriber(request, user_mail_hash):
    if request.method == 'POST':
        form = SubscriptionChoiceForm(request.POST)
        if form.is_valid():
            user_mail_obj = get_user_mail_obj(user_mail_hash)
            subscriber = get_existing_subscription(user_mail_obj.email)
            if subscriber is None:
                new_subscriber = form.save(commit=False)
                new_subscriber.email = user_mail_obj.email
                new_subscriber.save()
                form.save_m2m()  # saving many-to-many relationship as side effect of commit=false
                messages.success(request, 'You have been successfully subscribed')
            else:
                update_subscription(request, subscriber, form)
    else:
        form = SubscriptionChoiceForm()
    return render(request, "_confirm_subscription.html", {"form": form})


def page_not_found_view(request, exception):
    return render(request, '404.html', {"exception": exception})
    response.status_code = 404
    return response


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.password = make_password(password, None, 'md5')
            user.save()
    else:
        form = RegisterForm()
    return render(request, "register_user_form.html", {"form": form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Users.objects.get(email=email)
            encoded = user.password
            if check_password(password, encoded):
                messages.success(request, "You have been logged in successfully")
            else:
                messages.error(request, "Incorrect password")
    else:
        form = LoginForm()
    return render(request, "login_user_form.html", {"form": form})
