from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema.database import get_db
from schema.models import User, AuthProvider, OAuthRequest, AuthResponse, UserResponse
from datetime import datetime
import httpx
import jwt
from config import settings
import json

router = APIRouter()

# Google OAuth configuration
GOOGLE_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Facebook OAuth configuration
FACEBOOK_USER_INFO_URL = "https://graph.facebook.com/v12.0/me"

async def verify_google_token(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GOOGLE_USER_INFO_URL}?access_token={token}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        return response.json()

async def verify_facebook_token(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            FACEBOOK_USER_INFO_URL,
            params={
                "fields": "id,name,email,picture",
                "access_token": token
            }
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Facebook token"
            )
        return response.json()

def create_jwt_token(user_id: int) -> str:
    token_data = {
        "user_id": user_id,
        "exp": datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
    }
    return jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@router.post("/auth/{provider}", response_model=AuthResponse)
async def oauth_login(provider: AuthProvider, oauth_data: OAuthRequest, db: Session = Depends(get_db)):
    try:
        if provider == AuthProvider.GOOGLE:
            user_info = await verify_google_token(oauth_data.access_token)
            oauth_id = user_info["id"]
            email = user_info["email"]
            full_name = user_info["name"]
            profile_picture = user_info.get("picture")
        elif provider == AuthProvider.FACEBOOK:
            user_info = await verify_facebook_token(oauth_data.access_token)
            oauth_id = user_info["id"]
            email = user_info["email"]
            full_name = user_info["name"]
            profile_picture = user_info.get("picture", {}).get("data", {}).get("url")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OAuth provider"
            )

        # Check if user exists
        user = db.query(User).filter(
            (User.email == email) | 
            ((User.oauth_id == oauth_id) & (User.auth_provider == provider))
        ).first()

        if user:
            # Update existing user
            user.last_login = datetime.utcnow()
            if not user.oauth_id:
                user.oauth_id = oauth_id
                user.auth_provider = provider
            if profile_picture:
                user.profile_picture = profile_picture
        else:
            # Create new user
            user = User(
                email=email,
                full_name=full_name,
                oauth_id=oauth_id,
                auth_provider=provider,
                profile_picture=profile_picture,
                is_active=True,
                last_login=datetime.utcnow()
            )
            db.add(user)

        db.commit()
        db.refresh(user)

        # Generate JWT token
        token = create_jwt_token(user.user_id)

        return AuthResponse(
            success=True,
            token=token,
            user=UserResponse.model_validate(user)
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
