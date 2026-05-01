from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from authlib.jose import JsonWebKey

from django.conf import settings

knowns = NinjaAPI(urls_namespace="well-known")

@knowns.get('jwks.json', url_name="jwks")
def wk_jwks(request: HttpRequest, response: HttpResponse):
    response["Cache-Control"] = "public, max-age=86400, s-maxage=86400"

    key = JsonWebKey.import_key(settings.JWT_PUBLIC_KEY, {"kty": "EC"})

    jwks = {
        "keys": [
            {
                "kid": "v1",
                "use": "sig",
                "alg": settings.JWT_ALGORITHM,
                **key.as_dict(),
            }
        ]
    }

    return jwks