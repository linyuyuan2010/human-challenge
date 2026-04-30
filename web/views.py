from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

def show_challenge(request: HttpRequest):
    return render(request, "web/do_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})

def verify_challenge(request: HttpRequest):
    return render(request, "web/verify_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})