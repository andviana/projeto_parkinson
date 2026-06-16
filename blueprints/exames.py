import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import exam_service, patient_service

exames_bp = Blueprint('exames', __name__)

@exames_bp.route('/pacientes/<string:paciente_id>/exames/cadastro-rapido', methods=['GET', 'POST'])
@login_required
def cadastro_rapido_exames(paciente_id):
    details = patient_service.get_patient_details(paciente_id)
    if not details:
        abort(404)
        
    if request.method == 'POST':
        try:
            saved_exams = exam_service.cadastrar_exames(paciente_id, request.form)
            if saved_exams:
                flash(f"Exames salvos com sucesso para conferência rápida: {', '.join(saved_exams)}.", 'success')
            else:
                flash("Nenhum exame foi preenchido para salvamento.", 'warning')
                
            return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
        except Exception as e:
            flash(f'Erro ao salvar exames: {str(e)}', 'danger')
            return redirect(url_for('exames.cadastro_rapido_exames', paciente_id=paciente_id))
            
    data_hoje = datetime.date.today().strftime('%Y-%m-%d')
    return render_template('cadastro_exames.html', paciente=details['paciente'], data_hoje=data_hoje)
