from db import supabase

def list_all_patients():
    res = supabase.table('pacientes').select('*').order('nome_completo').execute()
    return res.data


def get_patient_by_id(paciente_id):
    res = supabase.table('pacientes').select('*').eq('id', paciente_id).execute()
    return res.data[0] if res.data else None


def create_patient(nome_completo, data_nascimento, sexo, tipo):
    data = {
        'nome_completo': nome_completo,
        'data_nascimento': data_nascimento,
        'sexo': sexo,
        'tipo': tipo
    }
    res = supabase.table('pacientes').insert(data).execute()
    return res.data[0] if res.data else None


def update_patient(paciente_id, nome_completo, data_nascimento, sexo, tipo):
    data = {
        'nome_completo': nome_completo,
        'data_nascimento': data_nascimento,
        'sexo': sexo,
        'tipo': tipo
    }
    res = supabase.table('pacientes').update(data).eq('id', paciente_id).execute()
    return res.data[0] if res.data else None
