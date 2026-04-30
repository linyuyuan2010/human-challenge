from nanoid import generate
from httpx import AsyncClient
from django.http import HttpRequest
from ninja import NinjaAPI
from django.conf import settings
from django.core.cache import cache

from .schema import ChallengeResult, ChallengeResponse, CheckChallenge, CheckResponse

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