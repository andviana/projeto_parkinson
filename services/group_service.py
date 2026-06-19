from models import group_repo, patient_repo
from services.exceptions import ValidationError, ResourceNotFoundError
from services.utils import parse_date

def list_groups_with_counts():
    lista_grupos = group_repo.list_all_groups()
    for g in lista_grupos:
        vinculos = group_repo.get_vinculos_by_group_id(g['id'])
        g['vinculos_count'] = len(vinculos)
        g['vinculos'] = [0] * len(vinculos)
    return lista_grupos


def create_group(nome):
    if not nome or not nome.strip():
        raise ValidationError("O nome do grupo é obrigatório.")
    existing = group_repo.get_group_by_name(nome)
    if existing:
        raise ValidationError("Já existe um grupo com este nome cadastrado.")
    return group_repo.create_group(nome)


def update_group_name(grupo_id, novo_nome):
    if not novo_nome or not novo_nome.strip():
        raise ValidationError("O nome do grupo não pode ser vazio.")
    existing = group_repo.get_group_by_name(novo_nome)
    if existing and int(existing['id']) != int(grupo_id):
        raise ValidationError("Já existe outro grupo com esse nome.")
    return group_repo.update_group_name(grupo_id, novo_nome)


def get_group_details(grupo_id):
    grupo = group_repo.get_group_by_id(grupo_id)
    if not grupo:
        raise ResourceNotFoundError("Grupo não encontrado.")
        
    vinculos = group_repo.get_vinculos_by_group_id(grupo_id)
    for v in vinculos:
        v['paciente'] = patient_repo.get_patient_by_id(v['id_paciente']) or {}
        v['data_inicio'] = parse_date(v['data_inicio'])
        if v.get('data_fim'):
            v['data_fim'] = parse_date(v['data_fim'])
            
    return grupo, vinculos
