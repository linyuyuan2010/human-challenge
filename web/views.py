from django.http import HttpRequest
from django.shortcuts import render
from django.core import signing
from django.views.decorators.http import require_http_methods

from django.conf import settings

@require_http_methods(["GET"])
def show_challenge(request: HttpRequest):
    return render(request, "web/do_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})

@require_http_methods(["GET"])
def verify_challenge(request: HttpRequest):
    return render(request, "web/verify_challenge.html", {"site_key": settings.HCAPTCHA_SITEKEY})

@require_http_methods(["GET"])
def show_challenge_jwtmode(request: HttpRequest):
    sub = request.GET.get('sub')
    aud = request.GET.get('aud')
    nonce = request.GET.get('nonce')
    callback = request.GET.get('callback')
    method = request.GET.get('method', "get").lower()

    if not (sub and aud and nonce and callback):
        return render(request, "web/tips.html",
                      {
                          "title": "缺少参数",
                          "details": """可能缺少以下查询参数
                          sub aud nonce callback"""
        })
    
    if method not in ["get", "post"]:
        return render(request, "web/tips.html",
                      {
                          "title": "参数错误",
                          "details": """method 参数错误"""
        })

    sig = signing.dumps(
        {
            "sub":sub,
            "aud": aud,
            "nonce": nonce,
            "method": method,
         }
    )

    return render(request, "web/do_challenge_jwt.html", {
        "site_key": settings.HCAPTCHA_SITEKEY,
        "callback": callback,
        "sig": sig,
    })