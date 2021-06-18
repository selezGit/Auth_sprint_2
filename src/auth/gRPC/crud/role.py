
from db.db_models import Role
from sqlalchemy.orm import Session

from crud.base import CRUDBase


class CRUDRole(CRUDBase):
    def __init__(self):
        self.model = Role

    def get_all(self, db: Session, skip, limit):
        return db.query(Role).offset(skip).limit(limit).all()

role = CRUDRole()