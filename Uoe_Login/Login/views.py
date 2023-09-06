from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import random
import string
from .helpers import send_forget_password_mail
import uuid
from django.core.mail import EmailMessage
from django.core.exceptions import *
from .forms import *
from django.contrib.auth.forms import SetPasswordForm
# from django.contrib.auth.forms import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .token import *
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()
# token_generator = SetPasswordForm(User)

# Create your views here.


def home(request):
    return render(request, 'uoe/uoe.html')


@login_required(login_url='signin')
def about(request):
    return render(request, 'uoe/about.html')


@login_required(login_url='signin')
def blog(request):
    return render(request, 'uoe/blog.html')


@login_required(login_url='signin')
def contact(request):
    return render(request, 'uoe/contact.html')


@login_required(login_url='signin')
def course(request):
    return render(request, 'uoe/course.html')


def signin(request):
    if request.method == 'POST':
        user_obj = auth.authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user_obj is not None:
            auth.login(request, user_obj)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials!')
            return redirect('student')
    return render(request, 'uoe/signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user_obj = User.objects.create_user(
                    username=username, email=email, password=password)
                user_obj.set_password(password)
                user_obj.save()

                # create a user profile
                user_model = User.objects.get(username=username)
                profile_obj = UserProfile.objects.create(
                    user=user_model, id_user=user_model.id)
                profile_obj.save()
                messages.success(
                    request, 'An account has been created successfully')
                return redirect('signin')
        else:
            messages.info(request, 'Password do not much')
            return redirect('signup')

    return render(request, 'uoe/signup.html')


@login_required(login_url='signin')
def reset(request):
    if request.method == 'POST':
        # validating user with email and send mail
        try:
            user = UserProfile.objects.filter(email=request.POST.get('email'))
            user1 = UserProfile.objects.get(email=request.POST.get('email'))
            email = user[0].email
            token = str(uuid.uuid4())
            user1.forget_password_token = token
            user1.save()
            mail_subject = 'UOE - Your forget password link'
            email_from = settings.EMAIL_HOST_USER
            message = render_to_string('uoe/email_template.html', {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user1.pk)),
                'token': PasswordTokenGenerator.make_token(user1),
                'protocol': 'https' if request.is_secure() else 'http',

            })
            email = EmailMessage(mail_subject, message, email_from, to=[email])
            email.send(fail_silently=False)
            messages.success(request, 'An email has been sent to you   ')
            return redirect('signin')
        # message to user if not found in database
        except User.DoesNotExist:
            messages.error(request, 'An account with ' +
                           request.POST.get('email') + ' not found, re-try')
    return render(request, 'uoe/reset.html')


@login_required(login_url='signin')
def change_password(request, token, uidb64):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None
    if user is not None and PasswordTokenGenerator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user=user, data=request.POST)
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password2')
            if new_password != confirm_password:
                messages.error(request, 'Password do not match')
            if form.is_valid():
                form.save()
                print(111)
                messages.success(
                    request, 'password has been successfully changed, you can now login in with the new passord')
                return redirect('signin')
    form = CustomSetPasswordForm(user=user, data=request.POST)

    return render(request, 'uoe/change_password.html', {'form': form})


'''class  PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'signin'
    success_url = reverse_lazy('password_success')'''


@login_required(login_url='signin')
def student(request):
    return render(request, 'uoe/student.html')
