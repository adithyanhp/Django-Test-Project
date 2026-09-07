"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from myapp import views
from myapp.forms import UserPasswordResetForm 
from django.contrib.auth import views as auth_views 

from rest_framework import routers
from rest_framework.routers import DefaultRouter
from myapp.views import StudentViewSet

router = DefaultRouter()
router.register('myapp', StudentViewSet, basename='student')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.StudentView,name="studentlist"),
    path('st',views.Student_Form,name="student_form"),
    path('edit/<int:id>/', views.Student_Edit, name="student_edit"),
    path('delete/<int:id>/', views.Student_Delete, name="student_delete"),
    path('empd', views.EmployeeView,name="employeelist"),
    path('emp', views.Employee_Form, name="employee_form"),
    path('emp/edit/<int:id>/', views.Employee_Edit, name="employee_edit"),
    path('emp/delete/<int:id>/', views.Employee_Delete, name="employee_delete"),
    path('register', views.RegisterView, name='register'),
    path('login', views.LoginView, name='login'),
    path('home', views.Home, name='home'),
    path('logout', views.LogoutView, name='logout'),
    # 1. Page where you type your email address
    # REPLACE your old password_reset/ line with this:
    path('password_reset/', views.AutomatedPasswordResetView.as_view(
        template_name='myapp/password_reset.html',
        form_class=UserPasswordResetForm
    ), name='password_reset'),


    # 2. Page that loads your password_reset_confirm.html file when you click the link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myapp/password_reset_confirm.html',
        success_url='/login'  # Jumps back to login after you save your new password
    ), name='password_reset_confirm'),

    # path('student_api/', views.StudentList, name='student_api'),  # API endpoint for Student data
    # path('student_api/create/', views.StudentCreate, name='student_create'),  # API endpoint for creating a new Student

    path('', include(router.urls)),  # Include the router URLs for the StudentViewSet
]


