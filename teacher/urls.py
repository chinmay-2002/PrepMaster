from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),

path('teacher_student_view', views.teacher_student_view,name='teacher_student_view'),
path('rank_board_view', views.rank_board_view,name='rank_board_view'),


path('teacher_view_student_marks_view', views.teacher_view_student_marks_view,name='teacher_view_student_marks_view'),
path('teacher_view_marks_view/<int:pk>', views.teacher_view_marks_view,name='teacher_view_marks_view'),
path('teacher_check_marks_view/<int:pk>', views.teacher_check_marks_view,name='teacher_check_marks_view'),

path('upload-job/', views.upload_job_view, name='upload_job'),
path('job_list', views.job_list_view, name='job_list'),
path('admin_job', views.admin_job, name='admin_job'),
path('teacher_job', views.teacher_job, name='teacher_job'),
# path('apply-job/<int:job_id>/', views.apply_job_view, name='apply_job'),
path('update_job/<int:pk>', views.update_job_view, name='update_job'),
path('delete_job/<int:pk>/', views.delete_job_view, name='delete_job'),
path('job_applications/', views.job_applications_view, name='job_applications'),
path('manage_application/<int:application_id>/', views.manage_application_view, name='manage_application'),
]