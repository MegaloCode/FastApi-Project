from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client): # client ==> is form the fixure not the general app instance

#     res = client.get("/")

#     print(res) 

#     assert res.json().get("message") == "we are getting starting, hello world"

#     assert res.status_code == 200



def test_create_user(client):

    res = client.post("/users/", json={
            "email": "hello123@gmail.com", # if email is not unique or it's present in database , it will throw error in test
            "password": "password123"
    })
    
    new_user = schemas.UserOut(**res.json()) # check if we have the wanted schema for user
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user , client): # look at the fixture scope on website for this test 

    res = client.post("/login",data={
            "username": test_user["email"],
            "password": test_user["password"]
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token , settings.secret_key , algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email , password , status_code " , [
     ("wrongemail@gmail.com" , "password123" , 403),
     ("hello123@gmail.com" , "wrongpassword" , 403),
     ("wrongemail@gmail.com" , "wrongpassword" , 403),
     (None , "password123" , 403), # status_code should be 403 , cuz you return 403 not 422 in all cases in your auth.py file
     ("hello123@gmail.com" , None , 403)
])
def test_incorrect_login(test_user , client , email , password , status_code):
    
        res = client.post("/login/" , data={
             "username": email ,
             "password": password}
             )
        
        assert res.status_code == status_code
        # assert res.json().get("detail") == "invalid credentials"