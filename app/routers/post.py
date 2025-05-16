from .. import models , schemas , oauth2
from typing import Optional , List , Dict , Any
from fastapi import FastAPI , Body , Response , status , HTTPException , Depends , APIRouter , Query
from ..database import engine , SessionLocal , get_db
from sqlalchemy.orm import Session
from sqlalchemy import func 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"])


# return all posts
# @router.get("/" ,response_model=list[schemas.Post]) # import list from typing module to convert response model to list
@router.get("/" , response_model=list[schemas.PostWithVotes]) # import list from typing module to convert response model to list
def get_posts(db: Session = Depends(get_db), limit: int = 10 , skip: int = 0 , search: Optional[str] = ""): # db: Session = Depends(get_db) ==> path operation function

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # convert results to dictionary
    posts_with_votes = []

    for post , votes in posts:

        post_dict = post.__dict__

        post_dict["votes"] = votes

        posts_with_votes.append(post_dict)

    return posts_with_votes



# return user's posts only
@router.get("/user-post" ,response_model=list[schemas.PostWithVotes]) # import list from typing module to convert response model to list
def get_posts(db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)): # path operation function

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts= db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()

    # convert results to dictionary
    posts_with_votes = []

    for post , votes in posts:

        post_dict = post.__dict__

        post_dict["votes"] = votes

        posts_with_votes.append(post_dict)

    return posts_with_votes



@router.get("/{id}" , response_model=schemas.PostWithVotes) # {id} ==> path parameter
def get_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # find a post with id either it belongs to user or not
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post , votes = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:

        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized to perform the requested action")
    
    # Convert SQLAlchemy model to dict and add votes
    post_dict = {**post.__dict__}
    post_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal field
    post_dict['votes'] = votes

    return post_dict



@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):

    print(current_user.email)

    new_post = models.Post(owner_id = current_user.id ,**post.dict()) # **post.dict() ==> (title=post.title , content=post.content , published=post.published)

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post



@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)  # either you add ==> .first() at the end of this code or

    post = post_query.first()

    if post == None: # add  ==> first at this statement

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="post not found")
    
    if post.owner_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized to perform the requested action")
    
    post_query.delete(synchronize_session=False) # or: db.delete(post) 

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int , updated_post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="post not found")
    
    if post.owner_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized to perform the requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()