from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

auth_register_parser = RequestParser(bundle_errors=True)
auth_register_parser.add_argument(name='login', type=str, location='form', required=True, nullable=False)
auth_register_parser.add_argument(name='email', type=email(check=True), location='form', required=True, nullable=False)
auth_register_parser.add_argument(name='password', type=str, location='form', required=True, nullable=False)


auth_login_parser = RequestParser(bundle_errors=True)
auth_login_parser.add_argument(name='login', type=str, location='form', required=True, nullable=False)
auth_login_parser.add_argument(name='password', type=str, location='form', required=True, nullable=False)

change_password_parser = RequestParser(bundle_errors=True)
change_password_parser.add_argument(name='old_password', type=str, location='form', required=True, nullable=False)
change_password_parser.add_argument(name='new_password', type=str, location='form', required=True, nullable=False)

change_email_parser = RequestParser(bundle_errors=True)
change_email_parser.add_argument(name='email', type=email(check=True), location='form', required=True, nullable=False)

delete_sn_parser = RequestParser(bundle_errors=True)
delete_sn_parser.add_argument(name='uuid', type=str, location='form', required=True, nullable=False, help='uuid социальной сети')

role_parser = RequestParser(bundle_errors=True)
role_parser.add_argument(name='user_id', type=str, location='form', required=True, nullable=False, help='id пользователя')
role_parser.add_argument(name='role_id', type=int, location='form', required=True, nullable=False, help='id роли')

create_role_parser = RequestParser(bundle_errors=True)
create_role_parser.add_argument(name='name', type=str, location='form', required=True, nullable=False, help='название роли')