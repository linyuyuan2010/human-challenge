from django.http import HttpRequest
from django.shortcuts import render
from django.core import signing

from django.conf import settings

def show_challenge(request: HttpRequest):
    return render(request, "web/do_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})

def verify_challenge(request: HttpRequest):
    return render(request, "web/verify_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})

def show_challenge_jwtmode(request: HttpRequest):
    sub = request.GET.get('sub')
    aud = request.GET.get('aud')
    nonce = request.GET.get('nonce')
    callback = request.GET.get('callback')

    sig = signing.dumps(
        {
            "sub":sub,
            "aud": aud,
            "nonce": nonce,
         }
    )

    return render(request, "web/do_challenge_jwt.html", {
        "site_key": settings.HCAPTCHA_SITEKEY,
        "callback": callback,
        "sig": sig,
    })