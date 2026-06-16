from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import group_service

grupos_bp = Blueprint('grupos', __name__)

@grupos_bp.route('/grupos', methods=['GET', 'POST'])
@login_required
def grupos():
    if request.method == 'POST':
        nome = request.form.get('nome')
        success, message = group_service.create_group(nome)
        if success:
            flash(message, 'success')
            return redirect(url_for('grupos.grupos'))
        else:
            flash(message, 'danger')
            
    lista_grupos = group_service.list_groups_with_counts()
    return render_template('grupos.html', grupos=lista_grupos)


@grupos_bp.route('/grupos/<int:grupo_id>/editar', methods=['POST'])
@login_required
def editar_grupo(grupo_id):
    novo_nome = request.form.get('nome')
    success, message = group_service.update_group_name(grupo_id, novo_nome)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('grupos.grupos'))


@grupos_bp.route('/grupos/<int:grupo_id>')
@login_required
def detalhes_grupo(grupo_id):
    grupo, vinculos = group_service.get_group_details(grupo_id)
    if not grupo:
        abort(404)
    return render_template('detalhes_grupo.html', grupo=grupo, vinculos=vinculos)
