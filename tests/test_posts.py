from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client , test_posts):
    res = authorized_client.get("/posts/")
    # posts = schemas.PostOut(res.json())  look at this line of code and try to solve this problem
    # now this is the solution ===>
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate , res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# test to know that unauthonticatd user is not able to retrieve posts
def test_unauthorized_user_get_all_posts(client , test_posts): # test_posts ==> use test_user automatically
    res = client.get("/posts/")
    assert res.status_code == 401 # for this line to work, i made get_posts api func to work with authentication , user should login


def test_unauthorized_user_get_one_post(client , test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client , test_posts):
    res = authorized_client.get(f"/posts/1231")
    assert res.status_code ==404


def test_get_one_post(authorized_client, test_posts):

    target_post = test_posts[0]

    res = authorized_client.get(f"/posts/{target_post.id}")

    assert res.status_code == 200

    # assert: payload shape & values
    post = schemas.PostOut(**res.json())

    assert post.id == target_post.id
    assert post.title == target_post.title
    assert post.content == target_post.content
    assert post.published == target_post.published

    # optional: if your schema includes votes and you know the expected count
    assert post.votes == 0



@pytest.mark.parametrize("title , content , published" , [
    (" awsome title " , " awsome content " , True),
    (" bad title " , " bad content " , False),
    (" good title " , " good content " , True)
])
def test_create_post(authorized_client , test_user , test_posts , title , content , published):

    res = authorized_client.post("/posts/", json={"title": title , "content": content , "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]



def test_create_post_default_published_true(authorized_client , test_posts , test_user):

    res = authorized_client.post("/posts/", json={"title": "hello newpy" , "content": "new content" })

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "hello newpy"
    assert created_post.content == "new content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]    



def test_unauthorized_user_create_post(client , test_posts , test_user):
    res = client.post("/posts/", json={"title": "hello newpy" , "content": "new content" })
    assert res.status_code == 401
    

def test_unauthorized_user_delete_post(client , test_posts , test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client , test_posts , test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client , test_posts , test_user):
    res = authorized_client.delete(f"/posts/12313124")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client , test_posts , test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client , test_posts , test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}" , json = data)
    updated_post = schemas.Post(**res.json())
    print(updated_post)
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]



def test_update_other_user_post(authorized_client , test_user , test_user2 , test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}" , json = data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client , test_posts , test_user):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client , test_posts , test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/12313124" , json = data)
    assert res.status_code == 404