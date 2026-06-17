from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import clinical_data_service, patient_service

clinical_data_bp = Blueprint('clinical_data', __name__)

@clinical_data_bp.route('/pacientes/<string:paciente_id>/dados-clinicos', methods=['GET', 'POST'])
@login_required
def dados_clinicos(paciente_id):
    # Verificar se o paciente existe
    paciente_details = patient_service.get_patient_details(paciente_id)
    if not paciente_details:
        abort(404)
        
    if request.method == 'POST':
        # Captura os campos selectMany do form
        sintomas_ids = request.form.getlist('sintomas_iniciais')
        localizacoes_ids = request.form.getlist('localizacao')
        
        success, message = clinical_data_service.save_clinical_data(
            paciente_id,
            request.form,
            sintomas_ids,
            localizacoes_ids
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
        else:
            flash(message, 'danger')
            
    # GET
    res = clinical_data_service.get_clinical_data(paciente_id)
    
    return render_template(
        'dados_clinicos.html',
        paciente=paciente_details['paciente'],
        dados_clinicos=res['dados_clinicos'],
        sintomas_dominio=res['sintomas_dominio'],
        localizacoes_dominio=res['localizacoes_dominio']
    )
