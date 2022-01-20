from datetime import datetime

from config import ABSTRACT_IP_GEOLOCATION_API_URL, ABSTRACT_HOLIDAYS_API_URL
from config.request import get_retry_request
from config.secrets import ABSTRACT_IP_GEOLOCATION_API_KEY, ABSTRACT_HOLIDAYS_API_KEY
from users.models import User
from config import ENVIRONMENT

requests = get_retry_request()


def get_holidays(country_code):
    current_dt = datetime.now()
    params = {
        'api_key': ABSTRACT_HOLIDAYS_API_KEY,
        'country': country_code,
        'year': current_dt.year,
        'month': current_dt.month,
        'day': current_dt.day
    }
    req = requests.get(ABSTRACT_HOLIDAYS_API_URL, params=params)
    return req.json()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def enrich_with_holiday_data(email, ip_address):
    if ENVIRONMENT == 'test':
        return
    req = requests.get(ABSTRACT_IP_GEOLOCATION_API_URL,
                       params={'api_key': ABSTRACT_IP_GEOLOCATION_API_KEY, 'ip_address': ip_address})
    location_data = req.json()
    country_code = location_data.get('country_code')
    if country_code is None:
        return
    holidays = get_holidays(country_code)
    if len(holidays) == 0:
        return
    holiday_name = holidays[0].get('name')
    user = User.objects.get(email=email)
    user.signup_holiday = holiday_name
    user.save()
    print(f"Holiday enrichment done for user [{email}]")
