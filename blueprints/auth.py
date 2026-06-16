from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from services import auth_service
from app_decorators import admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_obj = auth_service.authenticate_user(username, password)
        if user_obj:
            login_user(user_obj)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
            
        flash('Usuário ou senha incorretos.', 'danger')
        
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
@admin_required
def usuarios():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        success, message = auth_service.create_user(username, password, role)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.usuarios'))
        else:
            flash(message, 'danger')
            
    lista_usuarios = auth_service.list_users()
    return render_template('usuarios.html', usuarios=lista_usuarios)


@auth_bp.route('/usuarios/<int:user_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_usuario(user_id):
    success, message = auth_service.delete_user(user_id, current_user.id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('auth.usuarios'))
