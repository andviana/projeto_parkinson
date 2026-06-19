import re
from models import complementary_data_repo
from services.exceptions import ValidationError

def validate_and_sanitize_complementary_data(form_data):
    telefone_raw = form_data.get('telefone', '')
    if not telefone_raw:
        raise ValidationError("O campo telefone é obrigatório.")
        
    telefone_clean = re.sub(r'\D', '', str(telefone_raw))
    
    if len(telefone_clean) < 10 or len(telefone_clean) > 11:
        raise ValidationError("O telefone deve conter entre 10 e 11 dígitos numéricos.")

    dominio_manual = form_data.get('dominio_manual')
    if dominio_manual not in ['destro(a)', 'sinistro(a)']:
        raise ValidationError("Domínio manual inválido.")

    cor = form_data.get('cor')
    if cor not in ['pardo(a)', 'branco(a)', 'negro(a)', 'amarelo(a)']:
        raise ValidationError("Cor/Raça inválida.")

    estado_civil = form_data.get('estado_civil')
    if estado_civil not in ['solteiro(a)', 'casado(a)', 'separado(a)', 'viuvo(a)', 'divorciado(a)']:
        raise ValidationError("Estado civil inválido.")

    escolaridade = form_data.get('escolaridade')
    valid_escolaridade = [
        'fundamental incompleto', 'fundamental completo',
        'medio incompleto', 'medio completo',
        'superior incompleto', 'superior completo', 'pós graduação'
    ]
    if escolaridade not in valid_escolaridade:
        raise ValidationError("Nível de escolaridade inválido.")

    atividade_profissional = form_data.get('atividade_profissional')
    valid_atividades = [
        'aposentado(a)', 'desempregado(a)', 'trabalhador(a) ativo(a)',
        'auxilio doença', 'beneficiario(a)', 'amparo social'
    ]
    if atividade_profissional not in valid_atividades:
        raise ValidationError("Atividade profissional inválida.")

    sanitized_data = {
        'telefone': telefone_clean,
        'dominio_manual': dominio_manual,
        'cor': cor,
        'estado_civil': estado_civil,
        'escolaridade': escolaridade,
        'atividade_profissional': atividade_profissional
    }
    
    return sanitized_data


def get_complementary_data(paciente_id):
    return complementary_data_repo.get_dados_complementares(paciente_id)


def save_complementary_data(paciente_id, form_data):
    sanitized_data = validate_and_sanitize_complementary_data(form_data)
    return complementary_data_repo.save_dados_complementares(paciente_id, sanitized_data)


def format_telefone(tel):
    if not tel:
        return ""
    if len(tel) in [10, 11]:
        return f"{tel[:2]}-{tel[2:]}"
    return tel
