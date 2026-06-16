from db import supabase

def list_all_groups():
    res = supabase.table('grupos').select('*').order('nome').execute()
    return res.data


def get_group_by_name(nome):
    res = supabase.table('grupos').select('*').eq('nome', nome).execute()
    return res.data[0] if res.data else None


def get_group_by_id(grupo_id):
    res = supabase.table('grupos').select('*').eq('id', grupo_id).execute()
    return res.data[0] if res.data else None


def create_group(nome):
    res = supabase.table('grupos').insert({'nome': nome}).execute()
    return res.data[0] if res.data else None


def update_group_name(grupo_id, nome):
    res = supabase.table('grupos').update({'nome': nome}).eq('id', grupo_id).execute()
    return res.data[0] if res.data else None


def get_vinculos_by_group_id(grupo_id):
    res = supabase.table('vinculos_grupo').select('*').eq('id_grupo', grupo_id).execute()
    return res.data


def get_vinculo_by_id(vinculo_id):
    res = supabase.table('vinculos_grupo').select('*').eq('id', vinculo_id).execute()
    return res.data[0] if res.data else None


def get_active_vinculos_by_patient_and_group(paciente_id, grupo_id):
    # Supabase select. Mock adapter maps .eq() queries
    res = supabase.table('vinculos_grupo').select('*').eq('id_paciente', paciente_id).eq('id_grupo', grupo_id).execute()
    return [v for v in res.data if v['data_fim'] is None]


def create_vinculo(paciente_id, grupo_id, data_inicio):
    new_link = {
        'id_paciente': paciente_id,
        'id_grupo': grupo_id,
        'data_inicio': data_inicio
    }
    res = supabase.table('vinculos_grupo').insert(new_link).execute()
    return res.data[0] if res.data else None


def update_vinculo_end_date(vinculo_id, data_fim):
    res = supabase.table('vinculos_grupo').update({'data_fim': data_fim}).eq('id', vinculo_id).execute()
    return res.data[0] if res.data else None


def get_vinculos_by_patient_id(paciente_id):
    res = supabase.table('vinculos_grupo').select('*').eq('id_paciente', paciente_id).execute()
    return res.data
