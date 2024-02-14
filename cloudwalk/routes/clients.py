from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from cloudwalk.db.models import Client
from cloudwalk.schemas import Message,UserPublic, UserSchema
from cloudwalk.db.engine import get_session


router = APIRouter(prefix = '/users')


@router.post('/', response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = Client(
        status = user.status.value,
        batch = user.batch,
        credit_limit = user.credit_limit,
        interest_rate = user.interest_rate,
        denied_reason = user.denied_reason.value if user.denied_reason else None,
        denied_at = user.denied_at
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(Client).where(Client.user_id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.status = user.status.value
    db_user.batch = user.batch
    db_user.credit_limit = user.credit_limit
    db_user.interest_rate = user.interest_rate
    db_user.denied_reason = user.denied_reason.value if user.denied_reason else None
    db_user.denied_at = user.denied_at

    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(Client).where(Client.user_id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()
    return {'message': 'user deleted'}

