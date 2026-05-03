import time

from nanoid import generate
from httpx import AsyncClient
from django.http import HttpRequest, HttpResponse, JsonResponse
from ninja import NinjaAPI
from django.conf import settings
from django.core.cache import cache
from django.core import signing
from joserfc import jwt
from joserfc.jwk import ECKey

from .schema import ChallengeResult, ChallengeResponse, CheckChallenge, CheckResponse, ChallengeJWTResult

api = NinjaAPI(urls_namespace="api")

@api.post('submit-challenge/', url_name='submit', response=ChallengeResponse)
async def submit(request: HttpRequest, data: ChallengeResult):
    token = data.token

    async with AsyncClient() as client:
        result = await client.post(
            "https://api.hcaptcha.com/siteverify",
            data={
                "secret": settings.HCAPTCHA_SECRETKEY,
                "response": token,
                "sitekey": settings.HCAPTCHA_SITEKEY,
            }
        )

    if not result.json().get("success"):
        return {"success": False, "reason": "hCaptcha 说不行"}

    id = generate(size=8).upper()

    await cache.aset(f"challenge{id}", True, timeout=60)

    return {"success": True, "id": id}

@api.post('check-challenge/', url_name='check', response=CheckResponse)
async def check(request: HttpRequest, data: CheckChallenge):
    async with AsyncClient() as client:
        result = await client.post(
            "https://api.hcaptcha.com/siteverify",
            data={
                "secret": settings.HCAPTCHA_SECRETKEY,
                "response": data.hcaptcha_response,
                "sitekey": settings.HCAPTCHA_SITEKEY,
            }
        )
    code = data.code

    result = await cache.aget(f"challenge{code}", False)

    if result:
        await cache.adelete_many([f"challenge{code}"])

    return {"success": result}

@api.post('submit-challenge-jwt/', url_name='submit_jwt', response=ChallengeResponse)
async def submit_jwt(request: HttpRequest, data: ChallengeJWTResult):
    token = data.token

    async with AsyncClient() as client:
        result = await client.post(
            "https://api.hcaptcha.com/siteverify",
            data={
                "secret": settings.HCAPTCHA_SECRETKEY,
                "response": token,
                "sitekey": settings.HCAPTCHA_SITEKEY,
            }
        )

    if not result.json().get("success"):
        return {"success": False, "reason": "hCaptcha 说不行"}

    original: dict = signing.loads(data.sig)

    header = {
        "alg": settings.JWT_ALGORITHM,
        "kid": settings.JWT_KID,
    }

    payload = {
        "sub": original.get('sub'),
        "aud": original.get('aud'),
        "iss": settings.JWT_ISSUESER,
        "exp": int(time.time()) + settings.JWT_EXPIRING_IN,
        "iat": int(time.time()),
        "nonce": original.get('nonce'),
        "jti": generate(size=20).upper(),
        "verified": True,
    }

    key = ECKey.import_key(settings.JWT_PRIVATE_KEY)
    token = jwt.encode(header, payload, key, algorithms=[settings.JWT_ALGORITHM])
    return {"success": True, "id": token, "method": original.get('method')}

@api.get('public-key/', url_name='public_key')
def public_key(request: HttpRequest, response: HttpResponse):
    response["Cache-Control"] = "public, max-age=86400, s-maxage=86400"
    return {"payload": settings.JWT_PUBLIC_KEY}