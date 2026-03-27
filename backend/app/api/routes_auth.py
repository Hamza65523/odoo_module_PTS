from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token
from app.schemas.auth import TokenRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def token(payload: TokenRequest) -> TokenResponse:
    settings = get_settings()
    if payload.username != settings.pts_username or payload.password != settings.pts_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_value = create_access_token(subject=payload.username, extra_claims={"role": "admin"})
    return TokenResponse(access_token=token_value)
