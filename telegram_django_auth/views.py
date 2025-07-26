import io
from urllib.parse import urlparse, parse_qs

from django.http import JsonResponse, request
from django.shortcuts import render, redirect
from django.utils.translation import activate
from telethon.tl.custom import QRLogin

from telegram_django_auth import settings
from telegram_django_auth.countries import countries

from telethon import TelegramClient, errors
from telethon.sessions import StringSession

from asgiref.sync import async_to_sync

def telegram_view(request):
    return set_language_and_load(request)

# Replace these with your app's Telegram API credentials
API_ID = 20851336
API_HASH = "9965c9d43d7dae53c4d7d42cd22f21ac"

# Use a session with Telethon (use StringSession for flexibility)
SESSION = StringSession()
client = TelegramClient("SessionName", API_ID, API_HASH)

loginSessions = {}

# Global variable for storing the QR login session (can also store in Django sessions)
@async_to_sync
async def generate_qr_url(request) -> str:

    token = request.GET.get('token')
    if token:
        qrlo = loginSessions[token]
        return qrlo.url

    if not client.is_connected():
        await client.connect()

    # Ensure the client is not already authorized
    if not await client.is_user_authorized():
        # Get the QR Login object
        print("Client is not authorized. Generating QR login session...")
        qrlo = await client.qr_login()
        parsed_url = urlparse(qrlo.url)
        token = parse_qs(parsed_url.query)['token'][0]
        # Generate the QR login object
        loginSessions[token] = qrlo
        return qrlo.url
    else:
        print("Client is already authorized.")
        return ""

def qr_login_view(request):
    lang_code = request.session[settings.LANGUAGE_COOKIE_NAME]
    activate(lang_code)
    qr_url =  generate_qr_url(request)
    parsed_url = urlparse(qr_url)
    token = parse_qs(parsed_url.query)['token'][0]
    return render(request, 'login-qr.html',{'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'url': qr_url, 'token': token})

def qr_password(request):
    lang_code = request.session[settings.LANGUAGE_COOKIE_NAME]
    activate(lang_code)
    return render(request, 'login-qr-password.html',{'lang': request.session[settings.LANGUAGE_COOKIE_NAME]})

async def qr_wait_login(request):
    # Simulate data to be fetched
    data = {
        "timeout": False,
        "result": False,
        "password": False,
    }

    # Important! You need to wait for the login to complete!
    try:
        qrlo = loginSessions[request.GET.get('token')]
        data.result = await qrlo.wait(10)
    except TimeoutError:
        data["timeout"] = True
    except errors.SessionPasswordNeededError:
        data["password"] = True
    return JsonResponse(data)

def phone_login_view(request):
    lang_code = request.session[settings.LANGUAGE_COOKIE_NAME]
    activate(lang_code)
    return render(request, 'login-by-phone.html', {'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'countries': countries })

def set_language_and_load(request):
    """Activate the selected language from the button click."""
    lang_code = 'en'  # Get the language code from the query param
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    activate(lang_code)  # Activate the selected language
    qr_url = generate_qr_url(request)
    parsed_url = urlparse(qr_url)
    token = parse_qs(parsed_url.query)['token'][0]
    return render(request, 'login-qr.html', {'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'url': qr_url, 'token': token})

def change_language(request):
    """Activate the selected language from the button click."""
    lang_code = request.GET.get('lang', settings.LANGUAGE_CODE)  # Get the language code from the query param
    app = request.GET.get('app', 'qr')  # Get the language code from the query param
    if lang_code in dict(settings.LANGUAGES):  # Validate that the language is supported
        activate(lang_code)  # Activate the selected language
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code  # Persist the selection in the session
    return redirect('/'+app)
