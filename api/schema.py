from ninja import Schema

class ChallengeResult(Schema):
    token: str

class ChallengeResponse(Schema):
    success: bool
    id: str | None = None
    reason: str | None = None

class CheckChallenge(Schema):
    code: str
    hcaptcha_response: str

class CheckResponse(Schema):
    success: bool

class ChallengeJWTResult(Schema):
    token: str
    sig: str

class PublicKey(Schema):
    payload: str