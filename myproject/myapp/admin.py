from django.contrib import admin
from .models import Student, Teacher,Employee, Course, StudentProfile

# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(StudentProfile)
