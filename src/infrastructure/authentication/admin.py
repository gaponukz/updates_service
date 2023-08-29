import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security  import OAuth2PasswordBearer

load_dotenv()

def admin_required(api_key: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    if api_key != os.environ.get('ADMIN_PASSWORD_KEY'):
        print(api_key, os.environ.get('ADMIN_PASSWORD_KEY'))
        raise HTTPException(
            status_code=401,
            detail="Forbidden"
        )
