import datetime
import jwt
from django.conf import settings


def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'name': user.name,
        'phone': user.phone,
        'roles': user.roles,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
