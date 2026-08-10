# from django.shortcuts import render,redirect,get_object_or_404
# from .models import Student,Employee, Teacher,Course
# from .forms import EmployeeForm, RegistrationForm,LoginForm, StudentForm
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from .forms import UserPasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Employee, Teacher, Course
from .forms import EmployeeForm, RegistrationForm, LoginForm, StudentForm, UserPasswordResetForm
from django.contrib.auth import login, authenticate, logout  # Added logout
from django.contrib.auth.decorators import login_required

# Added modules required for password_reset_request to work without crashing
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages


def RegisterView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {"form": form})

# def LoginView(request):
#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             # Log the user in
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Redirect to home page after successful login
#     else:
#         form = LoginForm()
#     return render(request, 'myapp/login.html', {"form": form})
def LoginView(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {"form": form})

# NEW WORKFLOW: Handles the secure POST request sent from base.html
def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('home')

class AutomatedPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        associated_users = User.objects.filter(email=email)
        
        if associated_users.exists():
            user = associated_users.first()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # SUCCESS AUTOMATION: Instantly passes tokens to browser window
            return redirect('password_reset_confirm', uidb64=uid, token=token)
            
        # FIXED CRASH FALLBACK: If email is wrong, don't crash. Show an error banner instead!
        messages.error(self.request, "No registered account found with that email address.")
        return redirect('login')


@login_required
def Home(request):
    return render(request, 'myapp/home.html')


# Create your views here.
@login_required
def StudentView(request):
    student_data=Student.objects.all()
    # student_data=Student.objects.filter(age=20)  # Filter students with age 20
    return render(request,'myapp/studentlist.html',{"student_data":student_data})

@login_required
def Student_Form(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Safely extract all variables from cleaned_data
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            image = form.cleaned_data['image']
            teacher = form.cleaned_data['teacher']  # FIXED: Extracted teacher
            courses = form.cleaned_data['courses']  # FIXED: Extracted courses

            # 2. Create the student (Only assign ForeignKey 'teacher' here)
            student = Student.objects.create(
                name=name,
                age=age,
                email=email,
                teacher=teacher,
                image=image
            )

            # 3. Save ManyToMany relations (MUST use .set() after creation)
            student.courses.set(courses)  # FIXED: Linked courses safely
            
            return redirect('studentlist')
    else:
        form = StudentForm()
    return render(request, 'myapp/student_form.html', {"form": form})

            #Or 

# def Student_Form(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save() # FIXED: Automatically extracts and saves EVERYTHING correctly
#             return redirect('studentlist')
#     else:
#         form = StudentForm()
#     return render(request, 'myapp/student_form.html', {"form": form})

@login_required
def Student_Edit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student.name = form.cleaned_data['name']
            student.age = form.cleaned_data['age']
            student.email = form.cleaned_data['email']
            student.teacher = form.cleaned_data['teacher']
            student.courses.set(form.cleaned_data['courses'])
            
            # FIXED: Safely handle the clear checkbox or a new file upload
            new_image = form.cleaned_data['image']
            if new_image is False:
                # User checked the "Clear" checkbox
                student.image = None
            elif new_image:
                # User uploaded a new file
                student.image = new_image
            # If new_image is None, they left it alone (do not touch student.image)

            student.save()
            return redirect('studentlist')
    else:
        # FIXED: Converted courses.all to courses.all() with parenthesis so it fetches data correctly
        form = StudentForm(initial={
            'name': student.name,
            'age': student.age,
            'email': student.email,
            'teacher': student.teacher,
            'courses': student.courses.all(), # Added missing parenthesis
            'image': student.image
        })
    return render(request, 'myapp/student_form.html', {"form": form})


@login_required
def Student_Delete(request,id):
    student=get_object_or_404(Student,id=id)
    student.delete()
    return redirect('studentlist')

from django.shortcuts import get_object_or_404, redirect
from .models import Student, Teacher, Course

def assign_teacher_and_course(request, student_id):
    # 1. Fetch the specific student, teacher, and course
    student = get_object_or_404(Student, id=student_id)
    teacher = get_object_or_404(Teacher, id=1) # Replace with dynamic ID
    course = get_object_or_404(Course, id=2)   # Replace with dynamic ID

    # 2. Assign the single teacher (ForeignKey)
    student.teacher = teacher
    student.save() # Crucial: Save the student record after ForeignKey assignment

    # 3. Add the course (ManyToManyField)
    student.courses.add(course) # This automatically saves the relationship

    return redirect('student_list_view')



def EmployeeView(request):
    employee_data = Employee.objects.all()
    return render(request, 'myapp/employeelist.html', {"employee_data": employee_data})

def Employee_Form(request):
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()  # Saves only what is defined in EmployeeForm/Model
        return redirect('employeelist')
    return render(request, 'myapp/employee_form.html', {"form": form})

def Employee_Edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    # Passing instance=employee pre-populates fields and avoids AttributeErrors
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()  
        return redirect('employeelist')
    return render(request, 'myapp/employee_form.html', {"form": form})
def Employee_Delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employeelist')
