from .models import School,Student
from apps.user.models import EduUser
from apps.user.views import authorize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import jwt
import json
# Create your views here.


@csrf_exempt
@require_POST
def add_school(request):
    data = json.loads(request.body.decode('utf-8'))
    auth_info = authorize(request, roles=['school_owner'])

    if 'user_id' in auth_info:
        user_id = auth_info['user_id']
        user = get_object_or_404(EduUser, id=user_id)

        # Create the school and set school_applied_for
        school = School.objects.create(
            name=data.get('name'),
            owner=EduUser.objects.get(id=user_id),
            # parent=user,
            # school_applied_for_id=data.get('school_id'),
            # ... other fields
        )
        return JsonResponse({'message': 'School added successfully'}, status=201)
    else:
        return auth_info  # Return the unauthorized response

@csrf_exempt
@require_POST
def add_student(request):
    data = json.loads(request.body.decode('utf-8'))
    auth_info = authorize(request, roles=['parent'])

    if 'user_id' in auth_info:
        user_id = auth_info['user_id']
        user = get_object_or_404(EduUser, id=user_id)

    # Extract school information from the request data
        school_name = data.get('school_applied_for')

        # Check if the school exists in the School table
        school_exists = School.objects.filter(name=school_name).exists()

        if not school_exists:
            return JsonResponse({'error': 'School applied for does not exist in Edustoke'}, status=400)


        # Create the school and set school_applied_for
        student = Student.objects.create(
            name=data.get('name'),
            school_applied_for=data.get('school_applied_for'),
            class_applied_for=data.get('class_applied_for'),
            gender=data.get('gender'),
            parent=EduUser.objects.get(id=user_id),
            # ... other fields
        )
        return JsonResponse({'message': 'Student added for registration successfully'}, status=201)
    else:
        return auth_info  # Return the unauthorized response

@csrf_exempt
@require_http_methods(["PATCH"])
def update_student_admission_status(request):
    data = json.loads(request.body.decode('utf-8'))
    auth_info = authorize(request, roles=['school_owner'])

    if 'user_id' in auth_info:
        user_id = auth_info['user_id']

        # Check if the user owns a school with the provided name
        school_name = data.get('school_applied_for')
        owned_schools = School.objects.filter(owner=user_id, name=school_name)

        if owned_schools.exists():
            # Check if the requested school exists in the schools owned by the user
            school = owned_schools.filter(name=school_name).first()

            if school:
                # id field is the id of the student whose admission status is to be updated
                student_id = data.get('id')
                student = get_object_or_404(Student, id=student_id)
                # Check if the student's school_applied_for matches the provided school name
                if student.school_applied_for != school_name:
                    return JsonResponse({'error': 'Information mismatch for the student whose admission_status is to be updated'}, status=400)
                # Update admission status
                student.admission_status = data.get('admission_status')
                student.save()

                return JsonResponse({'message': 'Admission status updated successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Unauthorized'}, status=403)
        else:
            return JsonResponse({'message': 'Unauthorized'}, status=403)
    else:
        return auth_info  # Return the unauthorized response


@csrf_exempt
@require_GET
def registered_students(request):
    auth_info = authorize(request, roles=['school_owner'])

    if 'user_id' in auth_info:
        user_id = auth_info['user_id']

        # Get the schools owned by the user
        owned_schools = School.objects.filter(owner=user_id)
        print("owned_schools : ", owned_schools)
        # Get the admission_status parameter from the request, default to None
        admission_status = request.GET.get('admission_status', None)

        # Filter students based on admission_status if provided, else return all students
        students = Student.objects.filter(
            school_applied_for__in=owned_schools.values_list('name', flat=True),
        )
        print("all students  : ", students)
        if admission_status:
            students = students.filter(admission_status=admission_status)
        print("students admitted : ", students)
        # Return the list of students
        students_data = students.values('id', 'name', 'school_applied_for', 'class_applied_for', 'admission_status')
        return JsonResponse({'students': list(students_data)}, status=200)
    else:
        return auth_info  # Return the unauthorized response
