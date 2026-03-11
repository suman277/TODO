from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()
import os
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
class JWTUtils:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
    
    def create_access_token(self, username: str) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": username,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self.expire_minutes)).timestamp())
        }

        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
jwt_utils = JWTUtils(JWT_SECRET_KEY, "HS256", 30)  

def verify_token(
    creds: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = creds.credentials
    return jwt_utils.verify_access_token(token)