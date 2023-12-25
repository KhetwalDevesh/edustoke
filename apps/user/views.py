from .models import EduUser
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import jwt
import json
from utils.helpers import generate_jwt_token


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Assuming the data is sent as JSON
        data = json.loads(request.body.decode('utf-8'))
        print("data : ", data)
        name = data.get('name')
        password = data.get('password')
        phone = data.get('phone')
        roles = data.get('roles')  # Assuming roles are sent as a list in the request
        print("roles : ", roles)
        if not roles:
            return JsonResponse({'message': "'roles' is required"}, status=400)

        # Check if the phone is already taken
        if EduUser.objects.filter(phone=phone).exists():
            return JsonResponse({'message': 'Phone number already registered'}, status=400)

        # Create a new custom user with additional fields
        user = EduUser.objects.create(
            name=name,
            roles=roles,
            phone=phone,
            password=password,
            # ... other fields
        )
        user.save()

        # Generate and return the JWT token for the newly registered user
        token = generate_jwt_token(user)
        return JsonResponse({'token': token}, status=201)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        phone = data.get('phone')
        password = data.get('password')
        print("phone : ", phone)
        print("password : ", password)
        user = EduUser.objects.filter(phone=phone, password=password).first()

        if user is not None:
            token = generate_jwt_token(user)
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)


def authorize(request, roles=[]):
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]

    if not token:
        return JsonResponse({'message': 'Token missing'}, status=401)

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        name = decoded_token['name']
        phone = decoded_token['phone']
        user_roles = decoded_token['roles']

        if any(role in user_roles for role in roles):
            return {'user_id': user_id, 'name': name, 'phone': phone, 'roles': user_roles}
        else:
            return JsonResponse({'message': 'Unauthorized Role'}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'message': 'Invalid token'}, status=401)
