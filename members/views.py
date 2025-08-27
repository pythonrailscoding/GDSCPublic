import uuid

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from . import forms
from .models import VerifyMembers, Profile
from django.conf import settings


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = "@"+str(request.POST.get("user"))
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                request_user = User.objects.get(username=username)
                check_if_verify = VerifyMembers.objects.get(user=request_user)
                if check_if_verify.is_verified:
                    user_to_be_authenticated = auth.authenticate(username=username, password=password)
                    if user_to_be_authenticated is not None:
                        auth.login(request, user_to_be_authenticated)
                        messages.success(request, "You are now logged in!")
                        return redirect("index")
                    else:
                        messages.error(request, "Incorrect Password!")
                        return redirect("login")
                else:
                    messages.error(request, "Your account is not verified! Check your Registered Email to Verify!")
                    return redirect("login")
            else:
                messages.error(request, "No User exists with that username!")
                return redirect("login")
        return render(request, "members/login.html", {})
    else:
        messages.error(request, "You are already logged in!")
        return render(request, "main/index.html", {})

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user = "@"+str(request.POST["user"])
            f_name = request.POST["first_name"]
            l_name = request.POST["last_name"]
            email = request.POST["email"]
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]

            if User.objects.filter(username=user).exists():
                messages.error(request, "A user with that Username already exists")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "A user with that Email already exists")
                return redirect("register")
            else:
                if pass1 != pass2:
                    messages.error(request, "Passwords do not match")
                    return redirect("register")
                else:
                    token = uuid.uuid4()
                    new_user = User.objects.create_user(user, email, pass1, first_name=f_name, last_name=l_name)
                    VerifyMembers.objects.create(user=new_user, uid=token).save()
                    Profile.objects.create(user=new_user).save()
                    template = render_to_string("members/mail.html", {"user": user, "token": token})

                    send_mail(
                        "Verify Your Account",
                        template,
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
                    messages.success(request, "Account created! Please check your email to activate your account!")
                    return redirect("login")
        return render(request, "members/register.html", {})
    else:
        messages.error(request, "You are already Logged In! Logout to register.")
        return redirect("index")

def verify(request, token):
    print("Hello")
    if not request.user.is_authenticated:
        if VerifyMembers.objects.filter(uid=token).exists():
            user_to_be_verified = VerifyMembers.objects.get(uid=token)
            if user_to_be_verified.is_verified:
                messages.success(request, "You are already verified! You can login now!")
                return redirect("login")
            else:
                user_to_be_verified.is_verified = True
                user_to_be_verified.save()
                messages.success(request, "You are now verified! You can login now!")
                return redirect("login")
        else:
            messages.error(request, "The token is invalid or has expired! You can register again!")
            return redirect("register")
    else:
        messages.info(request, "You are already logged in!")
        return redirect("index")

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out!")
    return redirect("login")

class ChangeUserPassword(LoginRequiredMixin, PasswordChangeView):
    model = User
    template_name = "settings/change_password.html"
    form_class = forms.ChangeUserPasswordForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully changed!")
        return super().form_valid(form)

@login_required
def delete_user_account(request, token):
    if User.objects.filter(id=token).exists():
        user = User.objects.get(id=token)
        if user.id == request.user.id:
            if request.method == "POST":
                template = render_to_string("authentication/delete_mail.html", {"user": user.username})
                send_mail(
                    'Your account was deleted Successfully!',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                User.objects.get(id=request.user.id).delete()
                messages.success(request, "Account deleted Successfully! Hope to see you again")
                return redirect("register")
        else:
            messages.error(request, "You are not allowed to make changes to this form!")
            return redirect("index")
    else:
        messages.error(request, "This user doesn't exists!")
        return redirect("delete_user", pk=request.user.id)
    return render(request, "members/cancel_my_account.html", {})


def profile_user(request, pk):
    user = get_object_or_404(User, id=pk)
    profile_user_ = get_object_or_404(Profile, user=user)
    return render(request, "members/profile.html", {"user": user, "profile_user_": profile_user_})

@login_required
def settings_page(request):
    return render(request, 'members/setting_page.html', {})

@login_required
def update_user_profile(request, pk):
    user = get_object_or_404(User, id=pk)
    if not request.user.id == user.id:
        return redirect("update_user_profile", request.user.id)
    profile_user_ = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        user_change_form = forms.UserDetailsChangeForm(request.POST, instance=user)
        profile_user_change_form = forms.ProfileForm(request.POST, request.FILES, instance=profile_user_)

        if user_change_form.is_valid() and profile_user_change_form.is_valid():
            user_change_form.save()
            profile_user_change_form.save()
            return redirect("profile_user", user.id)
    else:
        user_change_form = forms.UserDetailsChangeForm(instance=user)
        profile_user_change_form = forms.ProfileForm(instance=profile_user_)
    return render(request, "members/update_profile.html" ,{"profile": profile_user_, "u_form": user_change_form, "p_form": profile_user_change_form})

