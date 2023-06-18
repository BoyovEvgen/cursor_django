from datetime import datetime, timedelta
import hashlib

from asgiref.sync import sync_to_async
from django.db.models import Q

from main.models import Discount_code
from ..models import DiscontSetings
from django.contrib.auth import get_user_model
User = get_user_model()


@sync_to_async
def create_promo_code(phone: str):
    discount_settings = DiscontSetings.objects.filter(Q(name='Telegram')).first()
    discount_code = Discount_code()
    string_to_hash: str= phone + str(datetime.now())
    discount_code.code = hashlib.sha3_256(string_to_hash.encode()).hexdigest()[:8]
    discount_code.discount = discount_settings.discount_percent
    discount_code.expiration_date = (datetime.now() + timedelta(discount_settings.days_of_validity or 365)).replace(second=0, microsecond=0)
    discount_code.is_active = True
    discount_code.for_user_phone = phone.lstrip('+')
    discount_code.save()
    return discount_code
