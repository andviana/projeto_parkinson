from werkzeug.security import generate_password_hash
from models import user_repo

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
        return False, "Dados inválidos."
        
    existing = user_repo.get_user_by_username(username)
    if existing:
        return False, "Este nome de usuário já está cadastrado."
        
    pw_hash = generate_password_hash(password)
    user_repo.create_user(username, pw_hash, role)
    return True, f"Usuário {username} cadastrado com sucesso."


def list_users():
    return user_repo.list_all_users()


def delete_user(user_id, current_user_id):
    if int(user_id) == int(current_user_id):
        return False, "Você não pode deletar sua própria conta ativa."
    user_repo.delete_user(user_id)
    return True, "Usuário removido com sucesso."
