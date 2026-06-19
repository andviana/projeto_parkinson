import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import exam_service, patient_service
from services.exceptions import ValidationError, ResourceNotFoundError

exames_bp = Blueprint('exames', __name__)

@exames_bp.route('/pacientes/<string:paciente_id>/exames/cadastro-rapido', methods=['GET', 'POST'])
@login_required
def cadastro_rapido_exames(paciente_id):
    try:
        details = patient_service.get_patient_details(paciente_id)
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        print(f"Erro ao obter detalhes do paciente {paciente_id}: {e}")
        abort(500)
        
    error_occurred = False
    if request.method == 'POST':
        try:
            saved_exams = exam_service.cadastrar_exames(paciente_id, request.form)
            if saved_exams:
                flash(f"Exames salvos com sucesso para conferência rápida: {', '.join(saved_exams)}.", 'success')
            else:
                flash("Nenhum exame foi preenchido para salvamento.", 'warning')
                
            return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
        except ValidationError as e:
            flash(str(e), 'danger')
            error_occurred = True
        except Exception as e:
            print(f"Erro ao cadastrar exames de {paciente_id}: {e}")
            flash('Erro ao tentar salvar exames.', 'danger')
            error_occurred = True
            
    data_hoje = datetime.date.today().strftime('%Y-%m-%d')
    status_code = 400 if error_occurred else 200
    return render_template('cadastro_exames.html', paciente=details['paciente'], data_hoje=data_hoje), status_code
