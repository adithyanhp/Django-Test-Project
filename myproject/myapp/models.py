from django.db import models

# Create your models here.

class Teacher(models.Model):
    name=models.CharField(max_length=25)
    age=models.IntegerField()
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    image = models.ImageField(upload_to='teacher_images/', blank=True, null=True) 
    
    def __str__(self):
                return self.name

class Course(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    
    def __str__(self):
                return self.name

class Student(models.Model):                #table creating in django
    name=models.CharField(max_length=25)
    age=models.IntegerField()
    email=models.EmailField()
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='students')
    courses=models.ManyToManyField(Course, related_name='students')
    image=models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
            return self.name

class StudentProfile(models.Model):
    student=models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    address=models.TextField()
    phone_number=models.CharField(max_length=15)
    date_of_birth=models.DateField()
    
    def __str__(self):
                return self.student.name



class Employee(models.Model):
    name=models.CharField(max_length=25)
    age=models.IntegerField()
    email=models.EmailField()
    designation=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    salary=models.FloatField()
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True) 
    
    def __str__(self):
                return self.name


     
    