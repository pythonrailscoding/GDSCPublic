from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

# autocomplete tells browser to check from already existing saved password (current-password)
# if (new-password), it will suggest

class ChangeUserPasswordForm(PasswordChangeForm):
	old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={
		'class': 'form-control', 'placeholder': 'Enter your old password','autocomplete': 'current-password',
	}))

	new_password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'new-password', 'type': 'password', 'placeholder': 'Enter your new password'}))
	new_password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'new-password', 'type': 'password', 'placeholder': 'Reconfirm your new password'}))

	class Meta:
		model = User
		fields = ('old_password', 'new_password1', 'new_password2',)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('user', 'bio', 'profile_pic', 'inst', 'twitter', 'facebook')

		widgets = {
			'user': forms.TextInput(attrs={'id': 'userid', 'type': 'hidden'}),
			'bio': forms.Textarea(attrs={}),
			'profile_pic': forms.FileInput(),
			'inst': forms.URLInput(),
			'twitter': forms.URLInput(),
			'facebook': forms.URLInput()
		}

class UserDetailsChangeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name')

		widgets = {
			'first_name': forms.TextInput(),
			'last_name': forms.TextInput(),
		}


