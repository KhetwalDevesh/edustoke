from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  add_school, add_student, update_student_admission_status, registered_students


urlpatterns = [
    path('register/', add_school, name='add_school'),
    path('register/student', add_student, name='add_student'),
    path('update_student_admission_status/', update_student_admission_status, name='update_student_admission_status'),
    path('registered_students/', registered_students, name='registered_students')
]
