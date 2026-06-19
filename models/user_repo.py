from flask_login import UserMixin
from werkzeug.security import check_password_hash
from db import supabase

class Usuario(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @property
    def is_admin(self):
        return self.role == 'admin'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def get_user_by_id(user_id):
    res = supabase.table('usuarios').select('*').eq('id', int(user_id)).execute()
    return res.data[0] if res.data else None


def get_user_by_username(username):
    res = supabase.table('usuarios').select('*').eq('username', username).execute()
    return res.data[0] if res.data else None


def list_all_users():
    res = supabase.table('usuarios').select('*').order('criado_em', desc=True).execute()
    return res.data


def create_user(username, password_hash, role):
    data = {
        'username': username,
        'password_hash': password_hash,
        'role': role
    }
    res = supabase.table('usuarios').insert(data).execute()
    return res.data[0] if res.data else None


def delete_user(user_id):
    supabase.table('usuarios').delete().eq('id', user_id).execute()


def check_db_connection():
    supabase.table('usuarios').select('id').limit(1).execute()
