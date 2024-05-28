from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from django.http import HttpResponseRedirect,HttpResponseNotFound


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

@login_required(login_url='teacherlogin')
def teacher_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'teacher/admin_student.html',context=dict)

@login_required(login_url='teacherlogin')
def teacher_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'teacher/admin_view_student_marks.html',{'students':students})

@login_required(login_url='teacherlogin')
def teacher_view_marks_view(request,pk):
    courses = QMODEL.Course.objects.all()
    response =  render(request,'teacher/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='teacherlogin')
def teacher_check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)

    results = QMODEL.Result.objects.filter(exam=course, student=student)

    # Retrieve all results for the given course
    all_results = QMODEL.Result.objects.filter(exam=course)

    # Sort results by marks
    sorted_results = sorted(all_results, key=lambda x: x.marks, reverse=True)

    # Calculate rank positions
    highest_marks = sorted_results[0].marks if sorted_results else 0
    medium_marks = sorted_results[len(sorted_results) // 2].marks if sorted_results else 0
    lowest_marks = sorted_results[-1].marks if sorted_results else 0

    return render(request, 'teacher/admin_check_marks.html', {
        'results': results,
        'all_results':all_results,
        'highest_marks': highest_marks,
        'medium_marks': medium_marks,
        'lowest_marks': lowest_marks,
        'course': course  # Pass the course object to the template
    })

def rank_board_view(request):
    all_results = QMODEL.Result.objects.all()

    # Group results by student
    results_by_student = {}
    for result in all_results:
        if result.student.id not in results_by_student:
            results_by_student[result.student.id] = {
                'student': result.student,
                'marks_list': [],
            }
        results_by_student[result.student.id]['marks_list'].append(result.marks)

    # Calculate average marks for each student
    for student_id, data in results_by_student.items():
        total_marks = sum(data['marks_list'])
        total_questions = len(data['marks_list']) * QMODEL.Question.objects.count()  # Assuming each mark is for one question
        data['average_marks_percentage'] = (total_marks / total_questions) * 100

    # Sort students based on their average marks
    sorted_students = sorted(results_by_student.values(), key=lambda x: x['average_marks_percentage'], reverse=True)

    return render(request, 'teacher/admin_rank_board.html', {
        'sorted_students': sorted_students
    })


# from .models import Job, JobApplication
# from .forms import JobForm, JobApplicationForm

@login_required(login_url='teacherlogin')
def teacher_job(request):
    return render(request,'teacher/teacher_job.html')


@login_required(login_url='adminlogin')
def admin_job(request):
    return render(request,'teacher/admin_job.html')

def upload_job_view(request):
    if request.method == 'POST':
        form = QFORM.JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # Assign the currently logged-in user
            job.save()
            message = "Upload Job Successfuly !!"
            return redirect('job_list')
    else:
        form = QFORM.JobForm()
    return render(request, 'teacher/upload_job.html', {'form': form})

def job_list_view(request):
    jobs = QFORM.Job.objects.all()
    return render(request, 'teacher/job_list.html', {'jobs': jobs})



def update_job_view(request, pk):
    job = QFORM.Job.objects.get(id=pk)
    jobForm = QFORM.JobForm(instance=job)
    if request.method == 'POST':
        jobForm = QFORM.JobForm(request.POST, instance=job)
        if jobForm.is_valid():
            jobForm.save()
            return redirect('job_list')  # Redirect to the job list page after updating
    return render(request, 'teacher/update_job.html', {'jobForm': jobForm})



def delete_job_view(request, pk):
    # Assuming you have a Job model and you want to delete an instance with the given pk
    try:
        job = QFORM.Job.objects.get(pk=pk)
        job.delete()
        # Redirect to a success URL after deletion
        return HttpResponseRedirect(reverse('job_list'))
    except QFORM.Job.DoesNotExist:
        # Handle case where the job instance does not exist
        return HttpResponseNotFound("The job you are trying to delete does not exist.")

def job_applications_view(request):
    applications = QFORM.JobApplication.objects.all()
    return render(request, 'teacher/job_applications.html', {'applications': applications})

def manage_application_view(request, application_id):
    application = QFORM.JobApplication.objects.get(id=application_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        return redirect('job_applications')
    return render(request, 'teacher/manage_application.html', {'application': application})