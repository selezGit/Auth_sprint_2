from db.db_models import SocialAccount
from sqlalchemy.orm import Session
from typing import Dict
from crud.base import CRUDBase


class CRUDSocialAccount(CRUDBase):
    def __init__(self):
        self.model = SocialAccount

    def get_by_social_id(self, db: Session, social_id: str, social_name: str):
        return db.query(SocialAccount.user_id).filter(SocialAccount.social_id == social_id,
                                                      SocialAccount.social_name == social_name).first()


socical_account = CRUDSocialAccount()
