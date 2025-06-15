"""
this file automatically imported to every file test (no need to import it in another test file)
the unique name of this file should be (""conftest.py")
"""

from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from alembic import command
from app import schemas
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


# def override_get_db(): # Dependency
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


"""
========>  loke at the comments in the code itself  <========
we can use ==> pytest --disable-warnings -v ==> to show only test results
we can use ==> pytest -v -x ==> stop testing after first test failed we face 
we use ==> pytest -v -s ==> -s there to print what is wrong with the test  
we can use res.json() ==> to print the actual data {"message": "we are getting starting ...."}
# we can get the message alone with ==> res.json().get("message")
========= we should run the test inside the docker container by this command ==>
# docker-compose -f docker-compose-dev.yml pytest --disable-warnings -v -s tests/test_users.py (not always working)
# you should change localhost name in database to localhost , cuz the current name ==> postgres will throw error 
"""

# client = TestClient(app)

"""
we create this fixture to fix the the error: this user is found in the database , not allowed double user_email
"""
"""
we can use alembic command
"""

# this fixture returning our database client or object
@pytest.fixture() # look at the fixture scope on website for this test 
def session():

    # clean our database before our test begins ==> then run this code: this way using sqlalchemy method
    Base.metadata.drop_all(bind=engine)

    # now we can run our code and create our tables ==> this way using sqlalchemy method
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.close()

# this fixture is returning my client
@pytest.fixture() # look at the fixture scope on website for this test 
def client(session):

    # # to create tables using alembic 
    # command.upgrade("head")

    def override_get_db(): # Dependency
        
        try:

            yield session

        finally:

            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app) # here we use yield not return to run code befor test
    
    # # to delete table useing alembic
    # command.downgrade("head")


@pytest.fixture
def test_user(client):

    user_data = {
            "email": "hello123@gmail.com",
            "password": "password123"
    }
    
    res = client.post("/users/" , json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):

    user_data = {
            "email": "hello@gmail.com",
            "password": "password123"
    }
    
    res = client.post("/users/" , json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client , token):
    client.headers = {
        **client.headers , 
        "Authorization": f"Bearer {token}",
    }

    return client


@pytest.fixture
def test_posts(test_user , session , test_user2):
    posts_data= [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"]
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2["id"]
        },
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model , posts_data)

    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.Post(title="first title" , content="first content", owner_id=test_user["id"]),
    #                  models.Post(title="second title" , content="second content", owner_id=test_user["id"]),
    #                  models.Post(title="third title" , content="third content", owner_id=test_user["id"])])
    
    session.commit()
    posts = session.query(models.Post).all()

    return posts