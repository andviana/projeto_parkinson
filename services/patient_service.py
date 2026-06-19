import datetime
from models import patient_repo, group_repo, exam_repo, clinical_data_repo
from services.exceptions import ValidationError, ResourceNotFoundError
from services.utils import parse_date

def list_patients():
    lista = patient_repo.list_all_patients()
    for p in lista:
        p['data_nascimento'] = parse_date(p['data_nascimento'])
    return lista


def create_patient(nome_completo, data_nasc_str, sexo, tipo):
    if not nome_completo or not data_nasc_str or not sexo or tipo not in ['HC', 'PR', 'PD']:
        raise ValidationError("Todos os campos de cadastro de paciente são obrigatórios.")
    try:
        parse_date(data_nasc_str)
        return patient_repo.create_patient(nome_completo, data_nasc_str, sexo, tipo)
    except ValueError as e:
        raise ValidationError(f"Data de nascimento inválida: {str(e)}") from e


def update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo):
    if not nome_completo or not data_nasc_str or not sexo or tipo not in ['HC', 'PR', 'PD']:
        raise ValidationError("Preencha todos os campos do formulário para editar.")
    try:
        parse_date(data_nasc_str)
        return patient_repo.update_patient(paciente_id, nome_completo, data_nasc_str, sexo, tipo)
    except ValueError as e:
        raise ValidationError(f"Data de nascimento inválida: {str(e)}") from e


def get_patient_details(paciente_id):
    paciente = patient_repo.get_patient_by_id(paciente_id)
    if not paciente:
        raise ResourceNotFoundError("Paciente não encontrado.")
        
    paciente['data_nascimento'] = parse_date(paciente['data_nascimento'])
    
    today = datetime.date.today()
    birth = paciente['data_nascimento']
    idade = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    
    vinculos = group_repo.get_vinculos_by_patient_id(paciente_id)
    for v in vinculos:
        v['grupo'] = group_repo.get_group_by_id(v['id_grupo']) or {}
        v['data_inicio'] = parse_date(v['data_inicio'])
        if v.get('data_fim'):
            v['data_fim'] = parse_date(v['data_fim'])
            
    grupos_ativos_ids = [v['id_grupo'] for v in vinculos if v['data_fim'] is None]
    grupos_all = group_repo.list_all_groups()
    grupos_disponiveis = [g for g in grupos_all if g['id'] not in grupos_ativos_ids]
    
    data_hoje = today.strftime('%Y-%m-%d')
    
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
            dt = parse_date(rx['data_exame'])
            exams_list.append({'tipo': display_name, 'data': dt, 'nota': float(rx['nota_final'])})
            
    exams_list.sort(key=lambda x: x['data'], reverse=True)
    
    dados_clinicos = clinical_data_repo.get_dados_clinicos(paciente_id)
    if dados_clinicos:
        sintomas_all = clinical_data_repo.get_sintomas_dominio()
        localizacoes_all = clinical_data_repo.get_localizacoes_dominio()
        
        sintomas_map = {s['id']: s['nome'] for s in sintomas_all}
        localizacoes_map = {l['id']: l['sigla'] for l in localizacoes_all}
        
        dados_clinicos['sintomas_nomes'] = [sintomas_map.get(sid) for sid in dados_clinicos.get('sintomas_ids', []) if sid in sintomas_map]
        dados_clinicos['localizacoes_nomes'] = [localizacoes_map.get(lid) for lid in dados_clinicos.get('localizacoes_ids', []) if lid in localizacoes_map]
    
    from services import complementary_data_service
    dados_comp = complementary_data_service.get_complementary_data(paciente_id)
    dados_comp_formatted_phone = complementary_data_service.format_telefone(dados_comp['telefone']) if dados_comp else ""

    return {
        'paciente': paciente,
        'idade': idade,
        'vinculos': vinculos,
        'grupos_disponiveis': grupos_disponiveis,
        'data_hoje': data_hoje,
        'exames': exams_list,
        'dados_clinicos': dados_clinicos,
        'dados_complementares': dados_comp,
        'dados_complementares_formatted_phone': dados_comp_formatted_phone
    }


def vincular_grupo(paciente_id, id_grupo, data_ini_str):
    if not id_grupo or not data_ini_str:
        raise ValidationError("Selecione o grupo e informe a data de início.")
    try:
        id_grupo_int = int(id_grupo)
        vinculos_ativos = group_repo.get_active_vinculos_by_patient_and_group(paciente_id, id_grupo_int)
        if vinculos_ativos:
            raise ValidationError("Este paciente já possui um vínculo ativo com o grupo selecionado.")
            
        group_repo.create_vinculo(paciente_id, id_grupo_int, data_ini_str)
    except ValueError as e:
        raise ValidationError("Grupo selecionado é inválido.") from e


def desligar_grupo(vinculo_id, data_fim_str):
    v = group_repo.get_vinculo_by_id(vinculo_id)
    if not v:
        raise ResourceNotFoundError("Vínculo não encontrado.")
        
    paciente_id = v['id_paciente']
    if not data_fim_str:
        raise ValidationError("Informe a data de desligamento.", context_id=paciente_id)
        
    data_inicio = parse_date(v['data_inicio'])
    try:
        data_fim = parse_date(data_fim_str)
    except ValueError as e:
        raise ValidationError(f"Data de desligamento inválida: {str(e)}", context_id=paciente_id) from e
    
    if data_fim < data_inicio:
        raise ValidationError("A data de fim não pode ser anterior à data de início do vínculo.", context_id=paciente_id)
        
    group_repo.update_vinculo_end_date(vinculo_id, data_fim_str)
    return paciente_id
