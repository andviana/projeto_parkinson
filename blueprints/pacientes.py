from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import patient_service

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['GET', 'POST'])
@login_required
def pacientes():
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        data_nasc_str = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        tipo = request.form.get('tipo')
        
        success, message = patient_service.create_patient(nome_completo, data_nasc_str, sexo, tipo)
        if success:
            flash(message, 'success')
            return redirect(url_for('pacientes.pacientes'))
        else:
            flash(message, 'danger')
            
    lista_pacientes = patient_service.list_patients()
    return render_template('pacientes.html', pacientes=lista_pacientes)


@pacientes_bp.route('/pacientes/<string:paciente_id>/editar', methods=['POST'])
@login_required
def editar_paciente(paciente_id):
    nome_completo = request.form.get('nome_completo')
    data_nasc_str = request.form.get('data_nascimento')
    sexo = request.form.get('sexo')
    tipo = request.form.get('tipo')
    
    success, message = patient_service.update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('pacientes.pacientes'))


@pacientes_bp.route('/pacientes/<string:paciente_id>')
@login_required
def detalhes_paciente(paciente_id):
    details = patient_service.get_patient_details(paciente_id)
    if not details:
        abort(404)
        
    return render_template('detalhes_paciente.html', 
                           paciente=details['paciente'], 
                           idade=details['idade'], 
                           vinculos=details['vinculos'], 
                           grupos_disponiveis=details['grupos_disponiveis'],
                           data_hoje=details['data_hoje'],
                           exames=details['exames'])


@pacientes_bp.route('/pacientes/<string:paciente_id>/vincular', methods=['POST'])
@login_required
def vincular_grupo(paciente_id):
    id_grupo = request.form.get('id_grupo')
    data_ini_str = request.form.get('data_inicio')
    
    success, message = patient_service.vincular_grupo(paciente_id, id_grupo, data_ini_str)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))


@pacientes_bp.route('/vinculos/<int:vinculo_id>/desligar', methods=['POST'])
@login_required
def desligar_grupo(vinculo_id):
    data_fim_str = request.form.get('data_fim')
    success, message, paciente_id = patient_service.desligar_grupo(vinculo_id, data_fim_str)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    if paciente_id:
        return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
    return redirect(url_for('pacientes.pacientes'))
