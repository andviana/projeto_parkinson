from db import supabase

def get_sintomas_dominio():
    res = supabase.table('sintomas_dominio').select('*').order('id').execute()
    return res.data if res.data else []


def get_localizacoes_dominio():
    res = supabase.table('localizacoes_dominio').select('*').order('id').execute()
    return res.data if res.data else []


def get_dados_clinicos(paciente_id):
    res = supabase.table('dados_clinicos').select('*').eq('id_paciente', paciente_id).execute()
    if not res.data:
        return None
        
    dados = res.data[0]
    
    # Buscar IDs de sintomas vinculados
    res_sintomas = supabase.table('dados_clinicos_sintomas').select('id_sintoma').eq('id_paciente', paciente_id).execute()
    dados['sintomas_ids'] = [item['id_sintoma'] for item in res_sintomas.data] if res_sintomas.data else []
    
    # Buscar IDs de localizações vinculadas
    res_locs = supabase.table('dados_clinicos_localizacoes').select('id_localizacao').eq('id_paciente', paciente_id).execute()
    dados['localizacoes_ids'] = [item['id_localizacao'] for item in res_locs.data] if res_locs.data else []
    
    return dados


def save_dados_clinicos(paciente_id, dados_principal, sintomas_ids, localizacoes_ids):
    # Verificar se já existe a ficha de dados clínicos do paciente
    res_exist = supabase.table('dados_clinicos').select('id_paciente').eq('id_paciente', paciente_id).execute()
    
    if res_exist.data:
        # Atualizar registro existente
        supabase.table('dados_clinicos').update(dados_principal).eq('id_paciente', paciente_id).execute()
    else:
        # Criar novo registro
        dados_principal['id_paciente'] = paciente_id
        supabase.table('dados_clinicos').insert(dados_principal).execute()
        
    # Atualizar relacionamento de sintomas (Deleta antigos e insere novos)
    supabase.table('dados_clinicos_sintomas').delete().eq('id_paciente', paciente_id).execute()
    if sintomas_ids:
        sintomas_data = [{'id_paciente': paciente_id, 'id_sintoma': int(sid)} for sid in sintomas_ids]
        supabase.table('dados_clinicos_sintomas').insert(sintomas_data).execute()
        
    # Atualizar relacionamento de localizações (Deleta antigos e insere novos)
    supabase.table('dados_clinicos_localizacoes').delete().eq('id_paciente', paciente_id).execute()
    if localizacoes_ids:
        locs_data = [{'id_paciente': paciente_id, 'id_localizacao': int(lid)} for lid in localizacoes_ids]
        supabase.table('dados_clinicos_localizacoes').insert(locs_data).execute()
        
    return True
