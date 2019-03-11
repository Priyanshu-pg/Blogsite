from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from posts.models import Post
from posts.models import UserMailIdMap
from datetime import datetime
from posts.forms import SubscribeUserForm, ConfirmSubscriberForm
from posts.utils import send_mail_to
from django.http import HttpResponse
import json
import math



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
            try:
                user_mail_id_map = UserMailIdMap.objects.get(email=current_email)
            except UserMailIdMap.DoesNotExist:
                user_mail_id_map = UserMailIdMap(email=current_email)
                user_mail_id_map.save()
            return send_mail_to(request, user_mail_id_map.email, user_mail_id_map.email_hash)

    else:
        form = SubscribeUserForm()
        return render(request, "_subscribe_form.html", {"form": form})


def confirm_subscriber(request, usermail):
    if request.method == 'POST':
        form = ConfirmSubscriberForm(request.POST)
        if form.is_valid():
            new_subscriber = form.save(commit=False)
            try:
                user_mail_obj = UserMailIdMap.objects.get(email_hash=usermail)
            except UserMailIdMap.DoesNotExist:
                raise Http404("No user email is registered. Please register again")
            new_subscriber.email = user_mail_obj.email
            new_subscriber.save()
            form.save_m2m()  # saving many-to-many relationship as side effect of commit=false
    else:
        form = ConfirmSubscriberForm()
    return render(request, "_confirm_subscription.html", {"form": form})


def page_not_found_view(request, exception):
    return render(request, '404.html', {"exception": exception})
    response.status_code = 404
    return response

