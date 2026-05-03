from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from joserfc import jwk

from django.conf import settings

knowns = NinjaAPI(urls_namespace="well-known")

@knowns.get('jwks.json', url_name="jwks")
def wk_jwks(request: HttpRequest, response: HttpResponse):
    response["Cache-Control"] = "public, max-age=86400, s-maxage=86400"

    key = jwk.import_key(settings.JWT_PUBLIC_KEY, key_type="EC", parameters={
        "use": "sig",
        "alg": "ES256",
        "kid": settings.JWT_KID,
    })

    jwks = {
        "keys": [
            key.as_dict(),
        ]
    }

    return jwks