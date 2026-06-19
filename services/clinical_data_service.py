from models import clinical_data_repo
from services.exceptions import ValidationError

def validate_and_sanitize_clinical_data(form_data):
    resposta_motora = form_data.get('resposta_motora')
    if resposta_motora and resposta_motora not in ['nenhuma melhora', 'pouca melhora', 'melhora parcial', 'melhora total']:
        raise ValidationError("Resposta motora inválida selecionada.")
        
    tolerancia_levodopa = form_data.get('tolerancia_levodopa')
    if tolerancia_levodopa and tolerancia_levodopa not in ['sem problemas', 'teve dificuldade', 'intolerancia']:
        raise ValidationError("Tolerância à levodopa inválida selecionada.")
        
    familiar_com_dp = form_data.get('familiar_com_dp', 'não')
    if familiar_com_dp not in ['sim', 'não', 'não sabe']:
        raise ValidationError("Histórico familiar de Parkinson inválido.")
        
    familiar_com_tremor = form_data.get('familiar_com_tremor', 'não')
    if familiar_com_tremor not in ['sim', 'não', 'não sabe']:
        raise ValidationError("Histórico familiar de tremor inválido.")

    tempo_sintomas = form_data.get('tempo_inicio_sintomas_anos')
    if tempo_sintomas and str(tempo_sintomas).strip() != '':
        try:
            tempo_sintomas = int(tempo_sintomas)
            if tempo_sintomas < 0:
                raise ValidationError("O tempo de início de sintomas deve ser um valor inteiro maior ou igual a 0.")
        except ValueError as e:
            raise ValidationError("O tempo de início de sintomas deve ser um valor inteiro válido.") from e
    else:
        tempo_sintomas = None

    uso_cafe = str(form_data.get('uso_regular_cafe', '')).lower() in ['true', 'on', '1', 'y', 'yes', 'checked']
    frequencia = form_data.get('frequencia_por_dia')
    if uso_cafe:
        if not frequencia or str(frequencia).strip() == '':
            raise ValidationError("A frequência por dia de café é obrigatória se o uso de café for ativo.")
        try:
            frequencia = int(frequencia)
            if frequencia <= 0:
                raise ValidationError("A frequência por dia de café deve ser um número inteiro positivo.")
        except ValueError as e:
            raise ValidationError("A frequência por dia de café deve ser um número inteiro válido.") from e
    else:
        frequencia = 0

    cirurgia_dp = str(form_data.get('cirurgia_dp', '')).lower() in ['true', 'on', '1', 'y', 'yes', 'checked']

    abuso_substancia = str(form_data.get('abuso_substancia', '')).lower() in ['true', 'on', '1', 'y', 'yes', 'checked']
    qual_substancia = form_data.get('qual_substancia', '').strip()
    if abuso_substancia:
        if not qual_substancia:
            raise ValidationError("A especificação da substância é obrigatória se houver abuso de substâncias.")
    else:
        qual_substancia = None

    ancestrais = form_data.get('ancestrais', '').strip() or None

    qual_familiar_dp = form_data.get('qual_familiar_dp', '').strip()
    if familiar_com_dp == 'sim':
        if not qual_familiar_dp:
            raise ValidationError("A especificação do familiar é obrigatória se houver familiar com Parkinson.")
    else:
        qual_familiar_dp = None

    qual_familiar_tremor = form_data.get('qual_familiar_tremor', '').strip()
    if familiar_com_tremor == 'sim':
        if not qual_familiar_tremor:
            raise ValidationError("A especificação do familiar é obrigatória se houver familiar com tremor.")
    else:
        qual_familiar_tremor = None

    sanitized_data = {
        'tempo_inicio_sintomas_anos': tempo_sintomas,
        'resposta_motora': resposta_motora or None,
        'tolerancia_levodopa': tolerancia_levodopa or None,
        'uso_regular_cafe': uso_cafe,
        'frequencia_por_dia': frequencia,
        'cirurgia_dp': cirurgia_dp,
        'abuso_substancia': abuso_substancia,
        'qual_substancia': qual_substancia,
        'ancestrais': ancestrais,
        'familiar_com_dp': familiar_com_dp,
        'qual_familiar_dp': qual_familiar_dp,
        'familiar_com_tremor': familiar_com_tremor,
        'qual_familiar_tremor': qual_familiar_tremor
    }
    
    return sanitized_data


def get_clinical_data(paciente_id):
    dados = clinical_data_repo.get_dados_clinicos(paciente_id)
    sintomas = clinical_data_repo.get_sintomas_dominio()
    localizacoes = clinical_data_repo.get_localizacoes_dominio()
    
    return {
        'dados_clinicos': dados,
        'sintomas_dominio': sintomas,
        'localizacoes_dominio': localizacoes
    }


def save_clinical_data(paciente_id, form_data, sintomas_ids, localizacoes_ids):
    sanitized_data = validate_and_sanitize_clinical_data(form_data)
    clinical_data_repo.save_dados_clinicos(paciente_id, sanitized_data, sintomas_ids, localizacoes_ids)
