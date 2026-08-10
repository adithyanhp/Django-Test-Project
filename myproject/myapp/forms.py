from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Employee, Student

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):        #To hide the help text in the register form
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your registered email address',
        })


# class StudentForm(forms.Form):
#     name=forms.CharField(max_length=25)
#     age=forms.IntegerField()
#     email=forms.EmailField()

#Or we can use ModelForm to create a form based on the Student model

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"  # or you can specify the fields you want to include, e.g.,
        # fields = ['name', 'age', 'email'] #

# class Employee(forms.Form):
#     name=forms.CharField(max_length=25)
#     age=forms.IntegerField()
#     email=forms.EmailField()
#     designation=forms.CharField()
#     department=forms.CharField()
#     salary=forms.FloatField()

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
       