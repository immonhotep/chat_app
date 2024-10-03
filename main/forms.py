from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class Signupform(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2')



    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter username',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        } ))
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter email address',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]',

    }))


    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }))
    
    password2 = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat Password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }))
    
class UserLoginForm(AuthenticationForm):


    def __init__(self,*args,**kwargs):
        super(UserLoginForm,self).__init__(*args,**kwargs)


    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter username',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
        } ))


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }))
    


class UpdateProfileForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields=('image','bio')

    
    bio = forms.CharField(widget=forms.Textarea(attrs={

        'placeholder':'Enter bio',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]',
    }))



class UpdateUserForm(forms.ModelForm):

    class Meta:

        model = User
        fields=('username','email','first_name','last_name')


    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Username',
        'class': 'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Enter Email address',
        'class': 'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))


    first_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter First Name',
        'class': 'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Last Name',
        'class': 'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
    }))


class ChangePasswordForm(PasswordChangeForm):


    old_password = forms.CharField(widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    })) 

    new_password1 = forms.CharField(label='New password ',widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old new password ',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    new_password2 = forms.CharField(label='Retype New Password',widget = forms.PasswordInput(attrs={

        'placeholder':'Repeat new password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    

