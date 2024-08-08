import json
import random
import secrets

import requests
import stripe
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from config.settings import EMAIL_HOST_USER, REMOTE_HOST, STRIPE_API_KEY, DEBUG, PROSTOR_LOGIN, PROSTOR_PASSWORD
from user_app.models import User


def send_mail_reg(user, host):
    token_verification = secrets.token_hex(16)
    user.token_verification = token_verification
    url = f"http://{host}/email-confirm/{user.token_verification}"
    send_mail(
        subject="Подверждение регистрации",
        message=f"Подтвердите регистрацию, перейдя по ссылке\n{url}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )


def email_confirm(request, token_verification):
    user = get_object_or_404(User, token_verification=token_verification)
    user.is_active = True
    user.token_verification = None
    user.save()
    return redirect(reverse('user_app:login'))


def send_auto_gen_password(request, context):
    email = request.POST['email']
    user = User.objects.get(email=email)
    new_password = secrets.token_hex(8)
    user.set_password(new_password)
    user.save()
    send_mail(
        message=f'Вот ваш новый пароль - \n{new_password}',
        subject='Новый пароль',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )


#############_STRIPE_#############

url = REMOTE_HOST

stripe.api_key = STRIPE_API_KEY


def new_create_stripe_session(price):
    if DEBUG:
        url = '127.0.0.1:8000'
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': price * 100,
                    'product_data': {
                        'name': 'Подписка на сервис Paid_content',
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=f'http://{url}/payment_success/',
    )
    return session.get('id'), session.get('url')


def send_sms(phone_number):
    random_code = random.randint(100000, 999999)
    post_url = 'http://api.prostor-sms.ru/messages/v2/send.json/'
    data = {
        "login": PROSTOR_LOGIN,
        "password": PROSTOR_PASSWORD,
        "messages": [
            {
                "phone": str(phone_number),
                "text": random_code,
                "clientId": "1"
            }
        ]
    }
    json_data = json.dumps(data)
    requests.post(post_url, data=json_data)
    return random_code
