import requests
import json

from app_main.models import Pupil
from app_users.models import SMSSentCount
from environs import Env
from django.http import JsonResponse

env = Env()
env.read_env()


def authorize():
    response = requests.post(url="https://notify.eskiz.uz/api/auth/login", data={
        "email": env.str('ESKIZ_EMAIL'),
        "password": env.str("ESKIZ_PASSWORD")
    })
    response = response.json()

    return (response["token_type"], response["data"]["token"])


def send_sms_to_pupils(request):
    data = json.loads(request.body)
    pupils_id = data.get("pupils")
    sms_text = data.get("text")
    token_type, token = authorize()

    for pupil_id in pupils_id:

        try:
            pupil_number = Pupil.objects.get(id=pupil_id).phone_number
            response = requests.request(method="POST", url="https://notify.eskiz.uz/api/message/sms/send", headers={
                'Authorization': f'{token_type.capitalize()} {token}'
            }, data={
                'mobile_phone': f"{pupil_number.country_code}{pupil_number.national_number}",
                'message': sms_text,
                'from': 'AL_XORAZMIY',
                'callback_url': ''
            }, files=[])

        except Exception as exp:
            print(f"{exp.__class__.__name__}: {exp}")
            pass

    return JsonResponse(data={'detail': 'Message was sent successfully'})
