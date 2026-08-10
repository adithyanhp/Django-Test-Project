from django.contrib import admin
from .models import Student, Teacher,Employee, Course, StudentProfile
from django.utils.html import format_html

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'teacher', 'Student_Image')
    search_fields = ('name', 'email')
    list_filter = ('teacher','name')
    filter_horizontal = ('courses',)
    fieldsets = (
        ('Student Information', {
            'fields': ('name', 'age', 'email','image')
        }),
        ('Academic Details', {
            'fields': ('teacher', 'courses')
        }),
    )
    save_on_top = True
    ordering = ('name',)
    list_per_page = 5
    def Student_Image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    Student_Image.short_description = 'Image'
# admin.site.register(Student, StudentAdmin)
admin.site.register(Employee)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(StudentProfile)


