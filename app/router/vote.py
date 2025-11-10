from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, security
from ..database import db

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(db: db, vote: schemas.Vote, current_user: int = Depends(security.get_current_user)):
    """
    Used to create a new vote or to delete an existing vote.

    Args:
        vote (schemas.Vote): The vote data to be created or deleted.
        current_user (int): The user id of the user who is creating or deleting the vote.

    Returns:
        dict: A dictionary containing a message indicating whether the vote was created or deleted successfully.

    Raises:
        HTTPException: If the post with the given id does not exist, if the user has already voted on the post (upvote), or if the vote does not exist (downvote).
    """
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id)
    # check if the vote exists or not
    found_vote = vote_query.first()

    # if we want to upvote
    if(vote.direction == 1):
        # if vote direction = 1 (upvote) and if vote is already present, then raise exception
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        # otherwise, it will be a new vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "upvoted successfully"}
    else:
        # if we want to downvote

        # if it was not upvoted, we can't downvote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        # otherwise, we downvote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "downvoted successfully"}
    
    