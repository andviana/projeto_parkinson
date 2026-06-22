import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import patient_service
from services.exceptions import ValidationError, ResourceNotFoundError

logger = logging.getLogger(__name__)

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['GET', 'POST'])
@login_required
def pacientes():
    status_code = 200
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        data_nasc_str = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        tipo = request.form.get('tipo')
        
        try:
            patient_service.create_patient(nome_completo, data_nasc_str, sexo, tipo)
            flash("Paciente cadastrado com sucesso.", 'success')
            return redirect(url_for('pacientes.pacientes'))
        except ValidationError as e:
            flash(str(e), 'danger')
            status_code = 400
        except Exception as e:
            logger.error(f"Erro inesperado ao criar paciente: {e}")
            flash("Erro interno do servidor ao cadastrar paciente.", 'danger')
            status_code = 500
            
    try:
        lista_pacientes = patient_service.list_patients()
        return render_template('pacientes.html', pacientes=lista_pacientes), status_code
    except Exception as e:
        logger.error(f"Erro ao listar pacientes: {e}")
        flash("Erro ao obter a lista de pacientes.", 'danger')
        return render_template('pacientes.html', pacientes=[]), 500


@pacientes_bp.route('/pacientes/<string:paciente_id>/editar', methods=['POST'])
@login_required
def editar_paciente(paciente_id):
    nome_completo = request.form.get('nome_completo')
    data_nasc_str = request.form.get('data_nascimento')
    sexo = request.form.get('sexo')
    tipo = request.form.get('tipo')
    
    try:
        patient_service.update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo)
        flash("Dados do paciente atualizados com sucesso.", 'success')
        return redirect(url_for('pacientes.pacientes'))
    except ValidationError as e:
        flash(str(e), 'danger')
        status_code = 400
    except ResourceNotFoundError as e:
        flash(str(e), 'danger')
        status_code = 404
    except Exception as e:
        logger.error(f"Erro inesperado ao editar paciente {paciente_id}: {e}")
        flash("Erro interno do servidor ao atualizar dados do paciente.", 'danger')
        status_code = 500
        
    try:
        lista_pacientes = patient_service.list_patients()
        return render_template('pacientes.html', pacientes=lista_pacientes), status_code
    except Exception as e:
        logger.error(f"Erro ao listar pacientes: {e}")
        flash("Erro ao obter a lista de pacientes.", 'danger')
        return render_template('pacientes.html', pacientes=[]), 500


@pacientes_bp.route('/pacientes/<string:paciente_id>')
@login_required
def detalhes_paciente(paciente_id):
    try:
        details = patient_service.get_patient_details(paciente_id)
        return render_template('detalhes_paciente.html', 
                               paciente=details['paciente'], 
                               idade=details['idade'], 
                               vinculos=details['vinculos'], 
                               grupos_disponiveis=details['grupos_disponiveis'],
                               data_hoje=details['data_hoje'],
                               exames=details['exames'],
                               dados_clinicos=details.get('dados_clinicos'),
                               dados_complementares=details.get('dados_complementares'),
                               dados_complementares_formatted_phone=details.get('dados_complementares_formatted_phone')), 200
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do paciente {paciente_id}: {e}")
        abort(500)


@pacientes_bp.route('/pacientes/<string:paciente_id>/vincular', methods=['POST'])
@login_required
def vincular_grupo(paciente_id):
    id_grupo = request.form.get('id_grupo')
    data_ini_str = request.form.get('data_inicio')
    
    try:
        patient_service.vincular_grupo(paciente_id, id_grupo, data_ini_str)
        flash("Paciente vinculado ao grupo com sucesso.", 'success')
        return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
    except ValidationError as e:
        flash(str(e), 'danger')
        status_code = 400
    except ResourceNotFoundError as e:
        flash(str(e), 'danger')
        status_code = 404
    except Exception as e:
        logger.error(f"Erro ao vincular grupo para paciente {paciente_id}: {e}")
        flash("Erro interno do servidor ao vincular paciente ao grupo.", 'danger')
        status_code = 500
        
    try:
        details = patient_service.get_patient_details(paciente_id)
        return render_template('detalhes_paciente.html', 
                               paciente=details['paciente'], 
                               idade=details['idade'], 
                               vinculos=details['vinculos'], 
                               grupos_disponiveis=details['grupos_disponiveis'],
                               data_hoje=details['data_hoje'],
                               exames=details['exames'],
                               dados_clinicos=details.get('dados_clinicos'),
                               dados_complementares=details.get('dados_complementares'),
                               dados_complementares_formatted_phone=details.get('dados_complementares_formatted_phone')), status_code
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do paciente {paciente_id}: {e}")
        abort(500)


@pacientes_bp.route('/vinculos/<int:vinculo_id>/desligar', methods=['POST'])
@login_required
def desligar_grupo(vinculo_id):
    data_fim_str = request.form.get('data_fim')
    paciente_id = None
    try:
        paciente_id = patient_service.desligar_grupo(vinculo_id, data_fim_str)
        flash("Paciente desligado do grupo com sucesso.", 'success')
        return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
    except ValidationError as e:
        flash(str(e), 'danger')
        paciente_id = e.context_id
        status_code = 400
    except ResourceNotFoundError as e:
        flash(str(e), 'danger')
        paciente_id = None
        status_code = 404
    except Exception as e:
        logger.error(f"Erro ao desligar vínculo {vinculo_id}: {e}")
        flash("Erro interno do servidor ao desligar paciente do grupo.", 'danger')
        paciente_id = None
        status_code = 500
        
    if paciente_id:
        try:
            details = patient_service.get_patient_details(paciente_id)
            return render_template('detalhes_paciente.html', 
                                   paciente=details['paciente'], 
                                   idade=details['idade'], 
                                   vinculos=details['vinculos'], 
                                   grupos_disponiveis=details['grupos_disponiveis'],
                                   data_hoje=details['data_hoje'],
                                   exames=details['exames'],
                                   dados_clinicos=details.get('dados_clinicos'),
                                   dados_complementares=details.get('dados_complementares'),
                                   dados_complementares_formatted_phone=details.get('dados_complementares_formatted_phone')), status_code
        except Exception as e:
            logger.error(f"Erro ao obter detalhes do paciente {paciente_id}: {e}")
            abort(500)
    else:
        try:
            lista_pacientes = patient_service.list_patients()
            return render_template('pacientes.html', pacientes=lista_pacientes), status_code
        except Exception as e:
            logger.error(f"Erro ao listar pacientes: {e}")
            flash("Erro ao obter a lista de pacientes.", 'danger')
            return render_template('pacientes.html', pacientes=[]), 500


