from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.database import async_session
from app.models import User
from sqlalchemy import select
import jwt
import httpx
from loguru import logger

security = HTTPBearer(auto_error=False)


async def verify_clerk_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")

    token = credentials.credentials

    try:
        if settings.clerk_jwt_pub_key:
            jwks_client = jwt.PyJWKClient(settings.clerk_jwt_pub_key)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={"verify_exp": True},
            )
            return payload

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.clerk.com/v1/sessions/verify",
                headers={"Authorization": f"Bearer {settings.clerk_api_key}"},
                params={"token": token},
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Auth verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_user(clerk_data: dict = Depends(verify_clerk_token)) -> User:
    clerk_id = clerk_data.get("sub", clerk_data.get("user_id", ""))
    if not clerk_id:
        raise HTTPException(status_code=401, detail="Invalid authentication data")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.clerk_id == clerk_id))
        user = result.scalar_one_or_none()

        if not user:
            email = clerk_data.get("email", clerk_data.get("email_addresses", [{}])[0].get("email_address", ""))
            name = clerk_data.get("name", clerk_data.get("first_name", "") + " " + clerk_data.get("last_name", ""))
            user = User(
                clerk_id=clerk_id,
                email=email,
                name=name.strip() or email.split("@")[0],
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
