import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from services import auth_service
from app_decorators import admin_required
from services.exceptions import ValidationError, ResourceNotFoundError

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user_obj = auth_service.authenticate_user(username, password)
            if user_obj:
                login_user(user_obj)
                flash('Login realizado com sucesso!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard.index'))
                
            flash('Usuário ou senha incorretos.', 'danger')
            return render_template('login.html'), 400
        except ValidationError as e:
            flash(str(e), 'danger')
            return render_template('login.html'), 400
        except Exception as e:
            logger.error(f"Erro inesperado de login: {e}")
            flash('Erro ao tentar fazer login. Tente novamente mais tarde.', 'danger')
            return render_template('login.html'), 500
        
    return render_template('login.html'), 200


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
    status_code = 200
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        try:
            auth_service.create_user(username, password, role)
            flash(f"Usuário {username} cadastrado com sucesso.", 'success')
            return redirect(url_for('auth.usuarios'))
        except ValidationError as e:
            flash(str(e), 'danger')
            status_code = 400
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            flash('Erro ao criar usuário no sistema.', 'danger')
            status_code = 500
            
    try:
        lista_usuarios = auth_service.list_users()
        return render_template('usuarios.html', usuarios=lista_usuarios), status_code
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        flash('Erro ao carregar lista de usuários.', 'danger')
        return render_template('usuarios.html', usuarios=[]), 500


@auth_bp.route('/usuarios/<int:user_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_usuario(user_id):
    status_code = 200
    try:
        auth_service.delete_user(user_id, current_user.id)
        flash("Usuário removido com sucesso.", 'success')
        return redirect(url_for('auth.usuarios'))
    except ValidationError as e:
        flash(str(e), 'danger')
        status_code = 400
    except ResourceNotFoundError as e:
        flash(str(e), 'danger')
        status_code = 404
    except Exception as e:
        logger.error(f"Erro ao deletar usuário {user_id}: {e}")
        flash('Erro ao tentar remover o usuário.', 'danger')
        status_code = 500

    try:
        lista_usuarios = auth_service.list_users()
        return render_template('usuarios.html', usuarios=lista_usuarios), status_code
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        flash('Erro ao carregar lista de usuários.', 'danger')
        return render_template('usuarios.html', usuarios=[]), 500


