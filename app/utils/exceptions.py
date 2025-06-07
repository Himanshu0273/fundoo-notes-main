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