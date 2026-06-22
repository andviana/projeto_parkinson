import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required
from services import clinical_data_service, patient_service
from services.exceptions import ValidationError, ResourceNotFoundError

logger = logging.getLogger(__name__)

clinical_data_bp = Blueprint('clinical_data', __name__)

@clinical_data_bp.route('/pacientes/<string:paciente_id>/dados-clinicos', methods=['GET', 'POST'])
@login_required
def dados_clinicos(paciente_id):
    try:
        paciente_details = patient_service.get_patient_details(paciente_id)
    except ResourceNotFoundError:
        abort(404)
    except Exception as e:
        logger.error(f"Erro ao carregar detalhes do paciente {paciente_id}: {e}")
        abort(500)
        
    status_code = 200
    if request.method == 'POST':
        sintomas_ids = request.form.getlist('sintomas_iniciais')
        localizacoes_ids = request.form.getlist('localizacao')
        
        try:
            clinical_data_service.save_clinical_data(
                paciente_id,
                request.form,
                sintomas_ids,
                localizacoes_ids
            )
            flash("Ficha de Dados Clínicos salva com sucesso!", 'success')
            return redirect(url_for('pacientes.detalhes_paciente', paciente_id=paciente_id))
        except ValidationError as e:
            flash(str(e), 'danger')
            status_code = 400
        except ResourceNotFoundError as e:
            flash(str(e), 'danger')
            status_code = 404
        except Exception as e:
            logger.error(f"Erro ao salvar dados clínicos de {paciente_id}: {e}")
            flash("Erro interno ao salvar dados clínicos. Tente novamente mais tarde.", 'danger')
            status_code = 500
            
    try:
        res = clinical_data_service.get_clinical_data(paciente_id)
    except Exception as e:
        logger.error(f"Erro ao obter dados clínicos de {paciente_id}: {e}")
        flash("Erro ao carregar dados clínicos cadastrados.", 'danger')
        res = {
            'dados_clinicos': None,
            'sintomas_dominio': [],
            'localizacoes_dominio': []
        }
        status_code = 500

    return render_template(
        'dados_clinicos.html',
        paciente=paciente_details['paciente'],
        dados_clinicos=res['dados_clinicos'],
        sintomas_dominio=res['sintomas_dominio'],
        localizacoes_dominio=res['localizacoes_dominio']
    ), status_code


