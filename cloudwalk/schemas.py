from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class DeniedSchema(Enum):
    MONEY_LOUNDRY = 'money_loundry'
    DEFAULTER = 'defaulter'
    ACCOUNT_TAKE_OVER = 'acccount_take_over'
    CRIMINAL_PROFILE = 'criminal_profile'


class StatusSchema(Enum):
    DENIED = 'denied'
    APROVED = 'approved'


class UserSchema(BaseModel):
    status: StatusSchema
    batch: int
    credit_limit: int
    interest_rate: int
    denied_reason: Optional[DeniedSchema] = None
    denied_at: Optional[datetime] = None


class UserPublic(BaseModel):
    user_id: int
    status: str
