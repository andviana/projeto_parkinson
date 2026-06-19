from db import supabase

def get_dados_complementares(paciente_id):
    res = supabase.table('dados_complementares').select('*').eq('id_paciente', paciente_id).execute()
    return res.data[0] if res.data else None


def save_dados_complementares(paciente_id, dados):
    # Verificar se já existe registro
    res_exist = supabase.table('dados_complementares').select('id_paciente').eq('id_paciente', paciente_id).execute()
    
    if res_exist.data:
        # Atualizar
        res = supabase.table('dados_complementares').update(dados).eq('id_paciente', paciente_id).execute()
    else:
        # Inserir
        dados['id_paciente'] = paciente_id
        res = supabase.table('dados_complementares').insert(dados).execute()
        
    return res.data[0] if res.data else None
