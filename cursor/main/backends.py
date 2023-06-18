from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username[1:-1].isdigit():
            phone_number = username
            if phone_number.startswith('+'):
                phone_number.lstrip('+')
            if phone_number.startswith('0') and len(phone_number) == 10:
                phone_number = '38' + phone_number
            user = User.objects.filter(Q(phone_number=phone_number)).first()
        else:
            user = User.objects.filter(Q(username=username)).first()
        if user and user.check_password(password):
            return user
        return None
