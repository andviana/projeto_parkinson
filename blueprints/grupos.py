from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import group_service
from services.exceptions import ValidationError, ResourceNotFoundError

grupos_bp = Blueprint('grupos', __name__)

@grupos_bp.route('/grupos', methods=['GET', 'POST'])
@login_required
def grupos():
    error_occurred = False
    if request.method == 'POST':
        nome = request.form.get('nome')
        try:
            group_service.create_group(nome)
            flash("Grupo cadastrado com sucesso.", 'success')
            return redirect(url_for('grupos.grupos'))
        except ValidationError as e:
            flash(str(e), 'danger')
            error_occurred = True
        except Exception as e:
            print(f"Erro inesperado ao criar grupo: {e}")
            flash("Erro interno do servidor ao criar grupo.", 'danger')
            error_occurred = True
            
    try:
        lista_grupos = group_service.list_groups_with_counts()
        status_code = 400 if error_occurred else 200
        return render_template('grupos.html', grupos=lista_grupos), status_code
    except Exception as e:
        print(f"Erro ao listar grupos: {e}")
        flash("Erro ao obter a lista de grupos.", 'danger')
        return render_template('grupos.html', grupos=[]), 500


@grupos_bp.route('/grupos/<int:grupo_id>/editar', methods=['POST'])
@login_required
def editar_grupo(grupo_id):
    novo_nome = request.form.get('nome')
    try:
        group_service.update_group_name(grupo_id, novo_nome)
        flash("Nome do grupo atualizado com sucesso.", 'success')
    except ValidationError as e:
        flash(str(e), 'danger')
    except Exception as e:
        print(f"Erro ao editar grupo {grupo_id}: {e}")
        flash("Erro interno do servidor ao editar grupo.", 'danger')
    return redirect(url_for('grupos.grupos'))


@grupos_bp.route('/grupos/<int:grupo_id>')
@login_required
def detalhes_grupo(grupo_id):
    try:
        grupo, vinculos = group_service.get_group_details(grupo_id)
        return render_template('detalhes_grupo.html', grupo=grupo, vinculos=vinculos), 200
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        print(f"Erro ao carregar detalhes do grupo {grupo_id}: {e}")
        abort(500)
