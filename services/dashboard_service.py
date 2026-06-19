from db import supabase
from models import user_repo, patient_repo
from services import group_service

def get_dashboard_data():
    db_status = "Conectado com Sucesso"
    is_mock = hasattr(supabase, 'db_path')
    db_type = "Local SQLite (Modo de Teste)" if is_mock else "Supabase Cloud (PostgreSQL)"
    
    try:
        user_repo.check_db_connection()
    except Exception as e:
        db_status = f"Erro de Conexão: {str(e)}"
        
    try:
        res_pacientes = patient_repo.get_all_patients_types()
        total_pacientes = len(res_pacientes)
        total_hc = sum(1 for p in res_pacientes if p['tipo'] == 'HC')
        total_pr = sum(1 for p in res_pacientes if p['tipo'] == 'PR')
        total_pd = sum(1 for p in res_pacientes if p['tipo'] == 'PD')
        
        lista_grupos = group_service.list_groups_with_counts()
    except Exception as e:
        print(f"Erro ao carregar estatísticas no dashboard: {e}")
        total_pacientes = total_hc = total_pr = total_pd = 0
        lista_grupos = []
        
    return {
        'db_status': db_status,
        'db_type': db_type,
        'total_pacientes': total_pacientes,
        'total_hc': total_hc,
        'total_pr': total_pr,
        'total_pd': total_pd,
        'grupos': lista_grupos
    }
