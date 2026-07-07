from fastapi import APIRouter, HTTPException, Query

from .auth_google import verify_google_credential
from .schemas import AuthResponse, GoogleAuthRequest, UserProfile
from .state import store

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google/verify", response_model=AuthResponse)
def auth_google_verify(body: GoogleAuthRequest) -> AuthResponse:
    try:
        profile = verify_google_credential(body.credential)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Google verification failed: {exc}") from exc

    if not profile.get("email"):
        raise HTTPException(status_code=400, detail="Google profile email not present")

    user = store.upsert_user(
        email=profile["email"],
        name=profile.get("name", "User"),
        picture=profile.get("picture"),
    )
    token = store.create_session(user.id)
    return AuthResponse(
        token=token,
        user=UserProfile(id=user.id, email=user.email, name=user.name, picture=user.picture),
    )


@router.get("/me", response_model=UserProfile)
def auth_me(token: str = Query(..., min_length=8)) -> UserProfile:
    user = store.get_user_by_session(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session token")
    return UserProfile(id=user.id, email=user.email, name=user.name, picture=user.picture)
