from fastapi import APIRouter , Depends , status , HTTPException , Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin , Token
from .. import models , utils , oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN , detail="invalid credentials")
    
    if not utils.verify(user_credentials.password , user.password):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN , detail="invalid credentials")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    # "bearer" means: "Anyone who has this token can access the protected resources."
    return {"access_token": access_token , "token_type": "bearer"} 