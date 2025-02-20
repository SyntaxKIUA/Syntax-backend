import requests
from django.conf import settings


def send_sms_kavenegar(receptor, message):
    api_key = settings.KAVENEGAR_API_KEY
    sender = settings.KAVENEGAR_SENDER
    url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"

    payload = {
        "receptor": receptor,
        "message": message,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception("somting wrong for opt!") from e

    return response.json()
