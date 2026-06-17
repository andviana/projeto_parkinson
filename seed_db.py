import os
import sys
from werkzeug.security import generate_password_hash

# Certifica que o diretório atual está no path do Python para importações locais
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db import supabase

def seed():
    print("--- INICIANDO SEMEAMENTO DO BANCO DE DADOS ---")
    
    # Verifica o tipo de conexão ativa
    is_mock = hasattr(supabase, 'db_path')
    db_type = "SQLite Local" if is_mock else "Supabase Cloud"
    print(f"Ambiente ativo: {db_type}")
    
    # 1. Inserção do Usuário Administrador Inicial
    print("\n[1/3] Verificando tabela de usuários...")
    try:
        res_user = supabase.table('usuarios').select('*').eq('username', 'admin').execute()
        if not res_user.data:
            admin_data = {
                'username': 'admin',
                'password_hash': generate_password_hash('Institutoviv@'),
                'role': 'admin'
            }
            supabase.table('usuarios').insert(admin_data).execute()
            print("✔ Usuário administrador ('admin' / 'Institutoviv@') criado com sucesso!")
        else:
            print("ℹ Usuário administrador ('admin') já existe. Nenhuma ação necessária.")
            
        # Cria clínico de testes padrão também
        res_clinico = supabase.table('usuarios').select('*').eq('username', 'clinico').execute()
        if not res_clinico.data:
            clinico_data = {
                'username': 'clinico',
                'password_hash': generate_password_hash('clinico'),
                'role': 'usuario'
            }
            supabase.table('usuarios').insert(clinico_data).execute()
            print("✔ Usuário clínico comum ('clinico' / 'clinico') criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao semear usuários: {e}")
        print("Certifique-se de criar a tabela 'usuarios' no Supabase antes de rodar o seed.")
        
    # 2. Inserção de Grupos Básicos
    print("\n[2/3] Verificando grupos de atividades...")
    try:
        res_grupos = supabase.table('grupos').select('*').execute()
        if len(res_grupos.data) == 0:
            grupos_basicos = [
                {'nome': 'Baila Parkinson'},
                {'nome': '3ª Idade Ativa'}
            ]
            supabase.table('grupos').insert(grupos_basicos).execute()
            print("✔ Grupos iniciais semeados com sucesso!")
        else:
            print(f"ℹ Grupos já existem no banco ({len(res_grupos.data)} cadastrados).")
    except Exception as e:
        print(f"❌ Erro ao semear grupos: {e}")

    # 3. Inserção de Domínios Clínicos
    print("\n[3/3] Verificando domínios de dados clínicos...")
    try:
        # Sintomas
        res_sintomas = supabase.table('sintomas_dominio').select('*').execute()
        if len(res_sintomas.data) == 0:
            sintomas = [
                {'nome': 'bradicinesia'},
                {'nome': 'rigidez'},
                {'nome': 'tremor'},
                {'nome': 'instabilidade postural'},
                {'nome': 'fraqueza muscular'},
                {'nome': 'formigamento'},
                {'nome': 'outros'}
            ]
            supabase.table('sintomas_dominio').insert(sintomas).execute()
            print("✔ Sintomas de domínio semeados com sucesso!")
        else:
            print(f"ℹ Sintomas de domínio já existem ({len(res_sintomas.data)} cadastrados).")
            
        # Localizações
        res_locs = supabase.table('localizacoes_dominio').select('*').execute()
        if len(res_locs.data) == 0:
            localizacoes = [
                {'sigla': 'MSD'},
                {'sigla': 'MIE'},
                {'sigla': 'MSE'},
                {'sigla': 'MS'},
                {'sigla': 'MI'},
                {'sigla': 'MID'},
                {'sigla': 'QUEIXO'},
                {'sigla': 'CABEÇA'},
                {'sigla': 'OUTRO'}
            ]
            supabase.table('localizacoes_dominio').insert(localizacoes).execute()
            print("✔ Localizações de domínio semeadas com sucesso!")
        else:
            print(f"ℹ Localizações de domínio já existem ({len(res_locs.data)} cadastradas).")
    except Exception as e:
        print(f"❌ Erro ao semear domínios clínicos: {e}")

    # 4. Mensagem de finalização
    print("\n--- PROCESSO DE SEMEAMENTO CONCLUÍDO ---")

if __name__ == '__main__':
    seed()
