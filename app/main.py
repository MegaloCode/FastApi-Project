from fastapi import FastAPI , APIRouter
from . import models
from .database import engine 
from .routers import post , user , auth , vote
from .config import settings  # setting ==> is the instance of the class not the class itself
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins= ["https://www.google.com" , "https://www.youtube.com"]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

    )

router = APIRouter()

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)


@app.get("/")
async def root():

    return {"message": "we are getting starting, just say 'go'"}


