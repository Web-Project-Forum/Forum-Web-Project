from fastapi import APIRouter, Header
from data.models import VoteModel, VoteUpDownMaps
from services import vote_service
from common.responses import BadRequest, Unauthorized, Forbidden
from common.auth import get_user_or_raise_401
from services import reply_service


votes_router = APIRouter(prefix='/votes')

@votes_router.post('/{reply_id}')
def create_vote(reply_id:int, vote_model:VoteModel, x_token: str | None = Header()):

    if not x_token:
        return Unauthorized(content='You are not authoriszed!')
    
    user = get_user_or_raise_401(x_token)


    if not reply_service.get_by_id(reply_id):
        return BadRequest(f'Reply {reply_id} doesn\'t exist!')
    
    if not vote_service.check_if_user_can_vote(reply_id, user.id):
        return BadRequest('You don\'t have permission to vote for this reply!')
    
    if vote_service.get_vote(reply_id, user.id):
        return BadRequest(f'You can change only your vote!')

    vote = vote_service.create(reply_id, user.id, vote_model)

    return vote
    

@votes_router.put('/{reply_id}')
def upgrade_vote(reply_id:int, vote_model:VoteModel, x_token: str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authoriszed!')
    
    user = get_user_or_raise_401(x_token)

    if not reply_service.get_by_id(reply_id):
        return BadRequest(f'Reply {reply_id} doesn\'t exist!')
    
    if not vote_service.check_if_user_can_vote(reply_id, user.id):
        return BadRequest('You don\'t have permission to vote for this reply!')
    

    old_vote = vote_service.get_vote(reply_id, user.id)
    
    if not old_vote:
         return create_vote(reply_id, vote_model, x_token)

    if old_vote.is_changed:
        return Forbidden(f'You can\'t change your vote anymore!')

    if old_vote.vote == VoteUpDownMaps.STR_TO_INT[vote_model.vote]:
        return BadRequest('Vote is the same as before!')

    data = vote_service.change_vote(old_vote, vote_model)

    return data


@votes_router.get('/{reply_id}')
def get_votes_total(reply_id:int):

    data = vote_service.total_vote(reply_id)

    return data

