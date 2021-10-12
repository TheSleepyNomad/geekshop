from django.shortcuts import render, HttpResponseRedirect
from django.urls.base import reverse_lazy
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from basketsapp.models import Basket
from geekshop.settings import DOMAIN_NAME, EMAIL_HOST_USER
from django.core.mail import send_mail
from .models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'title': 'Geekshop - Авторизация', 'form': form, }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid() and form.email_validation(request.POST['email']):
            x = form.save()
            if send_veify_link(x):
                messages.success(
                    request, 'Регистрация выполнена! На почту отправлена ссылка для подтверждения')
                return HttpResponseRedirect(reverse('users:login'))
        else:
            messages.error(request,
                           "Почта не прошла проверку доменного имени или такой почты не существует")
            form = UserRegistrationForm()
            context = {'title': 'Geekshop - Регистрация',
                       'form': form,
                       }
            return render(request, 'users/register.html', context)
    else:
        form = UserRegistrationForm()
        context = {'title': 'Geekshop - Регистрация',
                   'form': form,
                   }
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user,
                               data=request.POST, files=request.FILES)
        profile = UserProfileEditForm(
            data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile = UserProfileEditForm(
            data=request.POST, instance=request.user.userprofile)
    context = {'title': 'GeekShop - ЛК',
               'form': form,
               'profile_form': profile,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'users/profile.html', context)


def send_veify_link(user):
    verify_link = reverse(
        'users:verify', args=[user.email, user.activation_key])
    subject = f'Для активации учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, 'iluxaan@mail.ru', [user.email], fail_silently=False)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user and user.activation_key == activation_key and not user.is_activation_key_expired():
        user.activation_key = ''
        user.is_activation_key_expired = None
        user.is_active = True
        user.save()
        auth.login(request,
                   user,
                   backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'users/verification.html')
    else:
        return render(request, 'users/verification.html')
