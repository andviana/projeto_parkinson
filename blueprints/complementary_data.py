import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import complementary_data_service, patient_service
from services.exceptions import ValidationError, ResourceNotFoundError

logger = logging.getLogger(__name__)

complementary_data_bp = Blueprint('complementary_data', __name__)

@complementary_data_bp.route('/pacientes/<string:paciente_id>/dados-complementares', methods=['GET', 'POST'])
@login_required
def dados_complementares(paciente_id):
    try:
        paciente_details = patient_service.get_patient_details(paciente_id)
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        logger.error(f"Erro ao carregar detalhes do paciente {paciente_id}: {e}")
        abort(500)
        
    status_code = 200
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
            status_code = 400
        except ResourceNotFoundError as e:
            flash(str(e), 'danger')
            status_code = 404
        except Exception as e:
            logger.error(f"Erro ao salvar dados complementares de {paciente_id}: {e}")
            flash("Erro interno ao salvar dados complementares. Tente novamente mais tarde.", 'danger')
            status_code = 500
            
    try:
        res = complementary_data_service.get_complementary_data(paciente_id)
    except Exception as e:
        logger.error(f"Erro ao obter dados complementares de {paciente_id}: {e}")
        flash("Erro ao carregar dados complementares.", 'danger')
        res = None
        status_code = 500

    return render_template(
        'dados_complementares.html',
        paciente=paciente_details['paciente'],
        dados_complementares=res
    ), status_code


