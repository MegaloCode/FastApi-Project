from pydantic import BaseModel , EmailStr , conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):

    title: str

    content: str

    published: bool = True

    # rating: Optional[int] = None # should import Optional , cuz of the python version (import optional from typing module)

class PostCreate(PostBase):

    pass


class UserOut(BaseModel):

    id: int

    email: EmailStr

    created_at: datetime

    class Config:

        from_attributes = True


class Post(PostBase):

    id: int

    created_at: datetime

    owner_id: int

    owner: UserOut

    class Config:

        from_attributes = True 


class UserCreate(BaseModel):

    email: EmailStr

    password: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str

    class Config:

        from_attributes = True


class Token(BaseModel):

    access_token: str

    token_type: str


class TokenData(BaseModel):
    
    id: Optional[int] = None

class Vote(BaseModel):

    post_id: int

    # conint means integer must be less than or equal one , int <= 1 (0 , 1)
    dir: int = conint(le=1) # or use dirtype = conint(le=1) use variable then use it in the class
    

class PostWithVotes(PostBase):

    id: int

    votes: int

    class config:

        from_attributes= True

