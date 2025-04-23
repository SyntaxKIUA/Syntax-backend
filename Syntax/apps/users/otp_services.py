import requests
from django.conf import settings


def send_sms_kavenegar(receptor, message):
    API_KEY = settings.KAVENEGAR_API_KEY
    SENDER = settings.KAVENEGAR_SENDER
    url = (
        f"https://api.kavenegar.com/v1/{API_KEY}/Scope/MethodName.OutputFormat"
    )
    template = "forgotpassword"

    payload = {
        "sender": SENDER,
        "receptor": receptor,
        "message": message,
        # "template": template
    }

    try:
        response = requests.post(url, json=payload)
        print(response)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception("somting wrong for opt!") from e

    return response.json()
