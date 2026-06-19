from werkzeug.security import generate_password_hash
from models import user_repo
from services.exceptions import ValidationError

def authenticate_user(username, password):
    user = user_repo.get_user_by_username(username)
    if user:
        user_obj = user_repo.Usuario(
            id=user['id'], 
            username=user['username'], 
            password_hash=user['password_hash'], 
            role=user['role']
        )
        if user_obj.check_password(password):
            return user_obj
    return None


def create_user(username, password, role):
    if not username or not password or role not in ['usuario', 'admin']:
        raise ValidationError("Dados de cadastro inválidos.")
        
    existing = user_repo.get_user_by_username(username)
    if existing:
        raise ValidationError("Este nome de usuário já está cadastrado.")
        
    pw_hash = generate_password_hash(password)
    return user_repo.create_user(username, pw_hash, role)


def list_users():
    return user_repo.list_all_users()


def delete_user(user_id, current_user_id):
    if int(user_id) == int(current_user_id):
        raise ValidationError("Você não pode deletar sua própria conta ativa.")
    user_repo.delete_user(user_id)


def load_user(user_id):
    u = user_repo.get_user_by_id(user_id)
    if u:
        return user_repo.Usuario(
            id=u['id'], 
            username=u['username'], 
            password_hash=u['password_hash'], 
            role=u['role']
        )
    return None
