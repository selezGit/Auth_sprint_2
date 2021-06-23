import crud
from .db import get_db


def init_data():
    db = next(get_db())
    admin = crud.role.get_by(db=db, name='admin')
    if admin is None:
        crud.role.create(db=db, obj_in={'name': 'admin'})

    premium = crud.role.get_by(db=db, name='premium')
    if premium is None:
        crud.role.create(db=db, obj_in={'name': 'premium'})

    confirm = crud.role.get_by(db=db, name='confirm')
    if confirm is None:
        crud.role.create(db=db, obj_in={'name': 'confirm'})
    user = crud.user.get_by(db=db, login='admin')
    if user is None:
        data = {'login': 'admin', 'email': 'admin@gmail.com', 'password': '1'}
        role = crud.role.get_by(db=db, name='admin')
        crud.user.create(db=db, obj_in=data, role=role)
