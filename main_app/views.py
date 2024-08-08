import datetime

import stripe
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import handle_uploaded_file, image_verify, NoImageException

from config import settings
from config.settings import SUPPORT_EMAIL, STRIPE_WEBHOOK
from config.special_elements import PRICE_MONTH, PRICE_6_MONTH, PRICE_YEAR
from main_app.forms import PublicationForm
from main_app.models import Publication, Subscription
from main_app.services import new_create_stripe_session
from user_app.models import User, Payment
from user_app.views import CustomLoginRequiredMixin


class PublicationListView(ListView):
    model = Publication
    paginate_by = 5
    context_object_name = 'publications'
    template_name = 'main_app/index.html'

    def get_queryset(self):
        user = self.request.user
        try:
            if Subscription.objects.get(owner=user):
                return Publication.objects.order_by('-updated_at')
        except:
            return Publication.objects.all().filter(owner__subscription__isnull=True).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        user = self.request.user
        carousel_middle_text = 'Оформите подписку, для доступа к большей библиотеке публикаций'
        try:
            if Subscription.objects.get(owner=user):
                carousel_middle_text = 'Спасибо за оформление подписки!, Теперь вам доступно еще больше публикаций!'
                carousel_middle_text_hide = True
        except:
            carousel_middle_text_hide = False

        context = super().get_context_data(**kwargs)
        context['support_email'] = SUPPORT_EMAIL
        context['carousel_middle_text'] = carousel_middle_text
        context['carousel_middle_text_hide'] = carousel_middle_text_hide
        return context


class PublicationSearchView(ListView):
    context_object_name = 'publications'
    template_name = 'main_app/index.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user
        try:
            if Subscription.objects.get(owner=user):
                return Publication.objects.filter(owner__subscription__isnull=False).filter(
                    title__icontains=query).order_by('-updated_at')
        except:
            return Publication.objects.filter(title__icontains=query).filter(owner__subscription__isnull=True).order_by(
                '-updated_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p'] = self.request.GET.get('q')
        context['support_email'] = SUPPORT_EMAIL
        return context


class PublicationAuthorListView(ListView):
    context_object_name = 'publications'
    template_name = 'main_app/index.html'
    paginate_by = 5

    def get_queryset(self):
        author_id = self.kwargs.get('pk')
        author = get_object_or_404(User, pk=author_id)
        return Publication.objects.filter(owner=author).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['support_email'] = SUPPORT_EMAIL
        return context


class PublicationDetailView(DetailView):
    model = Publication


class PublicationCreateView(CustomLoginRequiredMixin, CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'main_app/publication_form.html'
    success_url = reverse_lazy('main_app:main')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PublicationUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm

    def get_success_url(self):
        return reverse_lazy('main_app:publication_detail', kwargs={'slug': self.object.slug})

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise Http404(_("Разрешено изменять только свои публикации"))
        return obj


class PublicationDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy('main_app:main')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise Http404(_("Разрешено удалять только свои публикации"))
        return obj


def upload_file(request):
    """
    Функция из .venv/lib/site-packages/django_ckeditor_5/view.py
    Пришлось ее переписать, так как библиотека запрещает загружать файлы, если user.is_staff=False
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES", False)

        if not allow_all_file_types:
            try:
                image_verify(request.FILES['upload'])
            except NoImageException as ex:
                return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            url = handle_uploaded_file(request.FILES["upload"])
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))


@login_required(login_url='user_app:login')
def buy_subscription(request):
    price_month = PRICE_MONTH
    price_6_month = PRICE_6_MONTH
    price_year = PRICE_YEAR

    total_price_6_month = price_6_month * 6
    total_price_year = price_year * 12

    id_session_month, url_month = new_create_stripe_session(price_month)
    Payment.objects.create(
        owner=request.user,
        session_id=id_session_month,
        price=price_month,
    )
    id_session_6_month, url_6_month = new_create_stripe_session(total_price_6_month)
    Payment.objects.create(
        owner=request.user,
        session_id=id_session_6_month,
        price=total_price_6_month,
    )
    id_session_year, url_year = new_create_stripe_session(total_price_year)
    Payment.objects.create(
        owner=request.user,
        session_id=id_session_year,
        price=total_price_year,
    )

    context = {
        'price_month': price_month,
        'price_6_month': price_6_month,
        'price_year': price_year,

        'total_price_6_month': total_price_6_month,
        'total_price_year': total_price_year,

        'url_month': url_month,
        'url_6_month': url_6_month,
        'url_year': url_year,

    }
    return render(request, 'main_app/subscription_create.html', context)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, STRIPE_WEBHOOK
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment = Payment.objects.get(session_id=session['id'])
        payment.is_paid = True
        payment.paid_at = timezone.now()
        payment.save()
        payments_list_to_remove = Payment.objects.filter(owner=payment.owner).filter(is_paid=False)
        for payment_to_remove in payments_list_to_remove:
            payment_to_remove.delete()

        if int(session['amount_total']) == PRICE_MONTH * 100:
            end_time = timezone.now() + datetime.timedelta(days=30)
        elif int(session['amount_total']) == PRICE_6_MONTH * 6 * 100:
            end_time = timezone.now() + datetime.timedelta(days=180)
        elif int(session['amount_total']) == PRICE_YEAR * 12 * 100:
            end_time = timezone.now() + datetime.timedelta(days=365)
        else:
            end_time = 'session["amount_total"] =! any of [PRICE_MONTH, PRICE_6_MONTH, PRICE_YEAR]'
        Subscription.objects.create(
            owner=payment.owner,
            is_active=True,
            update_at=timezone.now(),
            end_at=end_time
        )
    return HttpResponse(status=200)
