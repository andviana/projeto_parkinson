import datetime
from models import patient_repo, group_repo, exam_repo

def list_patients():
    lista = patient_repo.list_all_patients()
    for p in lista:
        p['data_nascimento'] = datetime.datetime.strptime(p['data_nascimento'].split(' ')[0], '%Y-%m-%d').date()
    return lista


def create_patient(nome_completo, data_nasc_str, sexo, tipo):
    if not nome_completo or not data_nasc_str or not sexo or tipo not in ['HC', 'PR', 'PD']:
        return False, "Todos os campos de cadastro de paciente são obrigatórios."
    try:
        # Validar formato de data
        datetime.datetime.strptime(data_nasc_str, '%Y-%m-%d').date()
        patient_repo.create_patient(nome_completo, data_nasc_str, sexo, tipo)
        return True, "Paciente cadastrado com sucesso."
    except Exception as e:
        return False, f"Erro ao cadastrar paciente: {str(e)}"


def update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo):
    if not nome_completo or not data_nasc_str or not sexo or tipo not in ['HC', 'PR', 'PD']:
        return False, "Preencha todos os campos do formulário para editar."
    try:
        datetime.datetime.strptime(data_nasc_str, '%Y-%m-%d').date()
        patient_repo.update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo)
        return True, "Dados do paciente atualizados com sucesso."
    except Exception as e:
        return False, f"Erro ao atualizar dados: {str(e)}"


def get_patient_details(paciente_id):
    paciente = patient_repo.get_patient_by_id(paciente_id)
    if not paciente:
        return None
        
    paciente['data_nascimento'] = datetime.datetime.strptime(paciente['data_nascimento'].split(' ')[0], '%Y-%m-%d').date()
    
    # Calcular idade dinamicamente
    today = datetime.date.today()
    birth = paciente['data_nascimento']
    idade = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    
    # Histórico de grupos vinculados
    vinculos = group_repo.get_vinculos_by_patient_id(paciente_id)
    for v in vinculos:
        v['grupo'] = group_repo.get_group_by_id(v['id_grupo']) or {}
        v['data_inicio'] = datetime.datetime.strptime(v['data_inicio'].split(' ')[0], '%Y-%m-%d').date()
        if v.get('data_fim'):
            v['data_fim'] = datetime.datetime.strptime(v['data_fim'].split(' ')[0], '%Y-%m-%d').date()
            
    # Filtragem de grupos disponíveis
    grupos_ativos_ids = [v['id_grupo'] for v in vinculos if v['data_fim'] is None]
    grupos_all = group_repo.list_all_groups()
    grupos_disponiveis = [g for g in grupos_all if g['id'] not in grupos_ativos_ids]
    
    data_hoje = today.strftime('%Y-%m-%d')
    
    # Consolidação do Histórico de Exames
    exams_list = []
    exam_types = {
        'gds': 'GDS',
        'moca': 'MoCA',
        'spdds': 'SPDDS',
        'updrs_i': 'UPDRS I',
        'updrs_ii': 'UPDRS II',
        'updrs_iii': 'UPDRS III',
        'updrs_iv': 'UPDRS IV',
        'hoehn_yahr': 'Hoehn & Yahr',
        'beck': 'Beck (BDI/BAI)'
    }
    
    for exam_key, display_name in exam_types.items():
        res_exams = exam_repo.get_exams_by_patient_and_table(exam_key, paciente_id)
        for rx in res_exams:
            dt = datetime.datetime.strptime(rx['data_exame'].split(' ')[0], '%Y-%m-%d').date()
            exams_list.append({'tipo': display_name, 'data': dt, 'nota': float(rx['nota_final'])})
            
    exams_list.sort(key=lambda x: x['data'], reverse=True)
    
    return {
        'paciente': paciente,
        'idade': idade,
        'vinculos': vinculos,
        'grupos_disponiveis': grupos_disponiveis,
        'data_hoje': data_hoje,
        'exames': exams_list
    }


def vincular_grupo(paciente_id, id_grupo, data_ini_str):
    if not id_grupo or not data_ini_str:
        return False, "Selecione o grupo e informe a data de início."
    try:
        id_grupo_int = int(id_grupo)
        vinculos_ativos = group_repo.get_active_vinculos_by_patient_and_group(paciente_id, id_grupo_int)
        if vinculos_ativos:
            return False, "Este paciente já possui um vínculo ativo com o grupo selecionado."
            
        group_repo.create_vinculo(paciente_id, id_grupo_int, data_ini_str)
        return True, "Paciente vinculado ao grupo com sucesso."
    except Exception as e:
        return False, f"Erro ao vincular grupo: {str(e)}"


def desligar_grupo(vinculo_id, data_fim_str):
    if not data_fim_str:
        return False, "Informe a data de desligamento.", None
    try:
        v = group_repo.get_vinculo_by_id(vinculo_id)
        if not v:
            return False, "Vínculo não encontrado.", None
            
        data_inicio = datetime.datetime.strptime(v['data_inicio'].split(' ')[0], '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        
        if data_fim < data_inicio:
            return False, "A data de fim não pode ser anterior à data de início do vínculo.", v['id_paciente']
            
        group_repo.update_vinculo_end_date(vinculo_id, data_fim_str)
        return True, "Paciente desligado do grupo com sucesso.", v['id_paciente']
    except Exception as e:
        return False, f"Erro ao registrar desligamento: {str(e)}", None
