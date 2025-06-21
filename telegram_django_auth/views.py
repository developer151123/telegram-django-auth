import io
from django.shortcuts import render, redirect
from django.utils.translation import activate

from telegram_django_auth import settings
from telegram_django_auth.countries import countries

from telethon import TelegramClient
from telethon.sessions import StringSession

from asgiref.sync import async_to_sync

def telegram_view(request):
    return set_language_and_load(request)


# Replace these with your app's Telegram API credentials
API_ID = 20851336
API_HASH = "9965c9d43d7dae53c4d7d42cd22f21ac"

# Use a session with Telethon (use StringSession for flexibility)
SESSION = StringSession()

# Global variable for storing the QR login session (can also store in Django sessions)
qr_login = None

@async_to_sync
async def generate_qr_url() -> str:

    global qr_login
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    # Ensure the client is not already authorized
    if not await client.is_user_authorized():
        # Get the QR Login object
        print("Client is not authorized. Generating QR login session...")
        qr_login = await client.qr_login()  # Generate the QR login object
        return qr_login.url
    else:
        print("Client is already authorized.")
        return ""


def qr_login_view(request):
    lang_code = request.session[settings.LANGUAGE_COOKIE_NAME]
    activate(lang_code)
    qr_url =  generate_qr_url()
    return render(request, 'login-qr.html', {'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'url': qr_url})

def phone_login_view(request):
    lang_code = request.session[settings.LANGUAGE_COOKIE_NAME]
    activate(lang_code)
    return render(request, 'login-by-phone.html', {'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'countries': countries })

def set_language_and_load(request):
    """Activate the selected language from the button click."""
    lang_code = 'en'  # Get the language code from the query param
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    activate(lang_code)  # Activate the selected language
    qr_url = generate_qr_url()
    return render(request, 'login-qr.html', {'lang': request.session[settings.LANGUAGE_COOKIE_NAME], 'url': qr_url})

def change_language(request):
    """Activate the selected language from the button click."""
    lang_code = request.GET.get('lang', settings.LANGUAGE_CODE)  # Get the language code from the query param
    app = request.GET.get('app', 'qr')  # Get the language code from the query param
    if lang_code in dict(settings.LANGUAGES):  # Validate that the language is supported
        activate(lang_code)  # Activate the selected language
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code  # Persist the selection in the session
    return redirect('/'+app)
