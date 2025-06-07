from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from ..schemas import auth_schema

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #make this a header


class AccessToken:
    def __init__(self,secret_key,    algorithm="HS256", time_expire=30):
        self.algorithm = algorithm
        self.time_expire = time_expire
        self.secret_key = secret_key
        
        
    def create_access_token(self, data: dict, expires_delta: timedelta|None=None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
            
            
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.time_expire)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


    def verify_access_token(self, token: str, credentials_exception):
        try:
            header = jwt.get_unverified_header(token)
            algo = header.get("alg", self.algorithm)
            
            payload = jwt.decode(token, self.secret_key, algorithms=[algo])
            username = payload.get("sub")
            if username is None: 
                raise credentials_exception
            
            token_data = auth_schema.TokenData(username=username, secret_key=self.secret_key)
        
        except JWTError:
            raise credentials_exception
        
        return token_data