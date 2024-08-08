from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from config.settings import DEBUG
from main_app.models import Publication, Subscription
from main_app.services import send_mail_reg, send_auto_gen_password, send_sms
from user_app.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserResetPasswordForm, \
    UserPasswordResetConfirmForm
from user_app.models import User


class CustomLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_app:login')
    redirect_field_name = 'redirect_to'


class UserLoginView(LoginView):
    form_class = UserLoginForm


class SMSVerificationView(View):

    def post(self, request):
        submitted_sms = request.POST.get('sms')
        saved_sms = request.session.get('sms')

        password = request.session.get('password1')
        email = request.session.get('email')
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')

        if submitted_sms == saved_sms:
            phone_number = request.session.get('phone_number')
            User = get_user_model()
            user = User.objects.create(
                phone_number=phone_number,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()
            return redirect('user_app:login')
        else:
            messages.error(request, 'Смс не верифицирован!')
            return render(request, 'user_app/register.html', {'form': UserRegisterForm(request.POST), 'sms_required': True})


class RegisterView(CreateView):
    def get(self, request, **kwargs):
        if request.session.get('sms'):
            form = UserRegisterForm()
        else:
            form = UserRegisterForm()
        return render(request, 'user_app/register.html', {'form': form, 'sms_required': False})

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone_number'])
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if 'sms' in request.POST:
                return SMSVerificationView.as_view()(request)
            else:
                password = form.cleaned_data['password1']
                if not DEBUG:
                    # sms = str(send_sms(phone_number))
                    sms = '1234'
                else:
                    sms = '1234'

                request.session['sms'] = sms
                request.session['phone_number'] = phone_number
                request.session['password1'] = password
                request.session['email'] = email
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                form.fields['password1'].widget.attrs['value'] = password
                form.fields['password2'].widget.attrs['value'] = password

                return render(request, 'user_app/register.html', {'form': form, 'sms_required': True})

        return render(request, 'user_app/register.html', {'form': form, 'sms_required': False})


class ProfileView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('user_app:profile')
    template_name = 'user_app/profile.html'

    def get_context_data(self, **kwargs):

        try:
            if Subscription.objects.get(owner=self.request.user):
                subscribe_hide = True
        except:
            subscribe_hide = False

        publications = Publication.objects.filter(owner=self.request.user)
        last_publications = publications.order_by('-updated_at')[:2]

        context = super().get_context_data(**kwargs)
        context['publications'] = publications
        context['last_publications'] = last_publications
        context['subscribe_hide'] = subscribe_hide
        return context


class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('user_app:profile', kwargs={'pk': self.object.pk})


class UserPasswordResetView(PasswordResetView):
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('user_app:password_reset_done')
    template_name = 'user_app/password_reset_form.html'
    email_template_name = 'user_app/password_reset_email.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'user_app/password_reset_confirm.html'
    success_url = reverse_lazy('user_app:password_reset_complete')


def user_auto_generate_password(request):
    context = {
        'reset_message': 'Новый пароль отправлен на почту'
    }
    if request.method == 'POST':
        send_auto_gen_password(request, context)
    return render(request, 'user_app/login.html', context)


def payment_success(request):
    return render(request, 'user_app/payment_success.html')
