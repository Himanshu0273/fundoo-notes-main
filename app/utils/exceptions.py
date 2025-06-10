from fastapi import HTTPException, status


#No user found
class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= f"No user with ID: {user_id} found!!"
        )
      
#Invalid Credentials  
class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials entered!!",
            headers={"WWW-Authenticate": "Bearer"}                
        )
    
#Email already exists      
class EmailAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The email: {email} already exists!!"
        )
        
#Username already exists
class UsernameAlreadyExistsException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The username: {username} already exists!!"
        )
        
#Unauthorized Access
class UnauthorizedAccessException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action!!"
        )
        
#Token Invalid
class TokenInvalidException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"}
        )        

#Token Expired
class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
        
#Regex Validation
class RegexValidationException(HTTPException):
    def __init__(self, field_name: str, error_msg: str):
        super().__init__(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} validation error: {error_msg}"
        )
        
#Env Exception       
class RequiredEnvVarError(Exception):
    """Non-HTTP exception for environment variables"""
    def _init_(self, var_name: str):
        super()._init_(f"Required environment variable '{var_name}' is not set")
        self.var_name = var_name