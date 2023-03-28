from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from app.utils import ALGORITHM, JWT_SECRET_KEY
from jose import jwt
from pydantic import ValidationError
from app.models import session,UserAccount
from fastapi.security import HTTPBearer

# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/login",
#     scheme_name="JWT"
# )

token_auth_scheme = HTTPBearer()


async def get_current_user(token: str = Depends(token_auth_scheme)):
    try:
        payload = jwt.decode(
            token.credentials, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        # if datetime.fromtimestamp(payload['exp']) < datetime.now():
        #     raise HTTPException(
        #         status_code = status.HTTP_401_UNAUTHORIZED,
        #         detail="Token expired",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.query(UserAccount).filter_by(email=payload['sub']).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user