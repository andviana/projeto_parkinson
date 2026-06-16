import datetime
from models import group_repo, patient_repo

def list_groups_with_counts():
    lista_grupos = group_repo.list_all_groups()
    for g in lista_grupos:
        vinculos = group_repo.get_vinculos_by_group_id(g['id'])
        g['vinculos_count'] = len(vinculos)
        # Manter compatibilidade com grupos.html listando mock arrays
        g['vinculos'] = [0] * len(vinculos)
    return lista_grupos


def create_group(nome):
    if not nome:
        return False, "O nome do grupo é obrigatório."
    existing = group_repo.get_group_by_name(nome)
    if existing:
        return False, "Já existe um grupo com este nome cadastrado."
    group_repo.create_group(nome)
    return True, "Grupo cadastrado com sucesso."


def update_group_name(grupo_id, novo_nome):
    if not novo_nome:
        return False, "O nome do grupo não pode ser vazio."
    existing = group_repo.get_group_by_name(novo_nome)
    if existing and int(existing['id']) != int(grupo_id):
        return False, "Já existe outro grupo com esse nome."
    group_repo.update_group_name(grupo_id, novo_nome)
    return True, "Nome do grupo atualizado com sucesso."


def get_group_details(grupo_id):
    grupo = group_repo.get_group_by_id(grupo_id)
    if not grupo:
        return None, []
        
    vinculos = group_repo.get_vinculos_by_group_id(grupo_id)
    for v in vinculos:
        v['paciente'] = patient_repo.get_patient_by_id(v['id_paciente']) or {}
        v['data_inicio'] = datetime.datetime.strptime(v['data_inicio'].split(' ')[0], '%Y-%m-%d').date()
        if v.get('data_fim'):
            v['data_fim'] = datetime.datetime.strptime(v['data_fim'].split(' ')[0], '%Y-%m-%d').date()
            
    return grupo, vinculos
