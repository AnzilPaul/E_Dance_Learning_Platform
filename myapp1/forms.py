from django import forms
from django.contrib.auth.models import User
from .models import UserRegInfo
from django.core import validators
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'}))
    full_name=forms.CharField(max_length=80,validators=[validators.MinLengthValidator(3,"Minimum 3 characters required!")],
    widget=forms.TextInput(attrs={'placeholder':'Full name', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'}))
    class Meta():
        model=User
        fields=('username','email','password')
        widgets={'username': forms.TextInput(attrs={'placeholder':'Username', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'})}
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
    def clean_username(self):
        username=self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError("Username must be atleast 4 characters.")
        return username
    def clean_password(self):
        password=self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
class UserRegInfoForm(forms.ModelForm):
    mobile_number=forms.CharField(max_length=15,required=True,validators=[validators.MinLengthValidator(10,"Enter valid mobile number.")],
    widget=forms.TextInput(attrs={'placeholder':'Mobile number', 'style':'background-color:#d6d3cf; width:400px; height:33px; border:0'}))
    class Meta():
        model=UserRegInfo
        fields=('mobile_number','home_address')
        widgets={'home_address': forms.Textarea(attrs={'placeholder':'Home address', 'style':'background-color:#d6d3cf; width:400px; height:66px; border:0'})}
    def clean_mobile(self):
        mobile_number=self.cleaned_data['mobile_number']
        if UserRegInfo.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("Mobile number already registered!")
        return mobile_number

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']       

