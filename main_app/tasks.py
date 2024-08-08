from celery import shared_task
from django.utils import timezone

from main_app.models import Subscription
from user_app.models import Payment


@shared_task
def check_subscriptions():
    all_subscriptions_list = Subscription.objects.all()
    for subscription in all_subscriptions_list:
        if subscription.end_at.date() <= timezone.now().date():
            subscription.delete()


@shared_task
def clear_residual_payments():
    all_payments_list = Payment.objects.filter(is_paid=False)
    for payment in all_payments_list:
        if payment.created_at.date() <= timezone.now().date():
            payment.delete()
