from typing import Any, Dict

import bcrypt
from db.db_models import User, Role
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from loguru import logger


class CRUDUser(CRUDBase):
    def __init__(self):
        self.model = User

    def check_password(self, user: User, password: str):
        return bcrypt.checkpw(password.encode(), user.password_hash.encode())

    def get_by(self, db: Session, **kwargs):
        return db.query(User).filter_by(**kwargs).first()

    def create(self, db: Session, *, obj_in: Dict, role=None) -> User:
        password = obj_in.pop('password')
        hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        password_hash = hash_bytes.decode('utf-8')
        db_obj = self.model(**obj_in)
        db_obj.password_hash = password_hash
        if role:
            db_obj.roles.append(role)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_social_account(self, db: Session, *, email: str, role: str = None) -> User:
        db_obj = self.model(email=email)
        if role:
            db_obj.roles.append(role)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_admin(self, db: Session, user_id):
        user = db.query(User).get(user_id)
        for role in user.roles:
            if role.name == 'admin':
                return True
        return False

    def remove_role(self, db: Session, user: User, role: Role):
        user.roles.remove(role)
        db.commit()

    def append_role(self, db: Session, user: User, role: Role):
        user.roles.append(role)
        db.add(user)
        db.commit()

    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Dict[str, Any],
    ) -> User:
        if obj_in.get('password'):
            password = obj_in.pop('password')
            hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            password_hash = hash_bytes.decode('utf-8')
            obj_in['password_hash'] = password_hash
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)


user = CRUDUser()
