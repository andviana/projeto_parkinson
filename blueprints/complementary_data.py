from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import complementary_data_service, patient_service
from services.exceptions import ValidationError, ResourceNotFoundError

complementary_data_bp = Blueprint('complementary_data', __name__)

@complementary_data_bp.route('/pacientes/<string:paciente_id>/dados-complementares', methods=['GET', 'POST'])
@login_required
def dados_complementares(paciente_id):
    try:
        paciente_details = patient_service.get_patient_details(paciente_id)
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        print(f"Erro ao carregar detalhes do paciente {paciente_id}: {e}")
        abort(500)
        
    error_occurred = False
    if request.method == 'POST':
        try:
            complementary_data_service.save_complementary_data(
                paciente_id,
                request.form
            )
            flash("Dados complementares salvos com sucesso!", 'success')
            return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
        except ValidationError as e:
            flash(str(e), 'danger')
            error_occurred = True
        except Exception as e:
            print(f"Erro ao salvar dados complementares de {paciente_id}: {e}")
            flash("Erro interno ao salvar dados complementares. Tente novamente mais tarde.", 'danger')
            error_occurred = True
            
    try:
        res = complementary_data_service.get_complementary_data(paciente_id)
    except Exception as e:
        print(f"Erro ao obter dados complementares de {paciente_id}: {e}")
        flash("Erro ao carregar dados complementares.", 'danger')
        res = None
        error_occurred = True

    status_code = 400 if error_occurred else 200
    return render_template(
        'dados_complementares.html',
        paciente=paciente_details['paciente'],
        dados_complementares=res
    ), status_code
