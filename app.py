import datetime
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required
from config import Config
from db import supabase
from models.user_repo import get_user_by_id, Usuario

# Inicialização global do Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        u = get_user_by_id(user_id)
        if u:
            return Usuario(id=u['id'], username=u['username'], password_hash=u['password_hash'], role=u['role'])
    except Exception as e:
        print(f"Erro ao carregar usuário no factory: {e}")
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa plugins
    login_manager.init_app(app)

    # Registro de Blueprints
    from blueprints.auth import auth_bp
    from blueprints.grupos import grupos_bp
    from blueprints.pacientes import pacientes_bp
    from blueprints.exames import exames_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(grupos_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(exames_bp)

    # Rota Central (Dashboard) registrada na raiz da aplicação
    @app.route('/')
    @login_required
    def index():
        db_status = "Conectado com Sucesso"
        is_mock = hasattr(supabase, 'db_path')
        db_type = "Local SQLite (Modo de Teste)" if is_mock else "Supabase Cloud (PostgreSQL)"
        
        try:
            # Validar integridade
            supabase.table('usuarios').select('id').limit(1).execute()
        except Exception as e:
            db_status = f"Erro de Conexão: {str(e)}"
            
        try:
            # Buscar estatísticas
            res_pacientes = supabase.table('pacientes').select('id, tipo').execute().data
            total_pacientes = len(res_pacientes)
            total_hc = sum(1 for p in res_pacientes if p['tipo'] == 'HC')
            total_pr = sum(1 for p in res_pacientes if p['tipo'] == 'PR')
            total_pd = sum(1 for p in res_pacientes if p['tipo'] == 'PD')
            
            # Buscar pacientes recentes
            pacientes_recentes = supabase.table('pacientes').select('*').order('criado_em', desc=True).limit(5).execute().data
            for p in pacientes_recentes:
                p['data_nascimento'] = datetime.datetime.strptime(p['data_nascimento'].split(' ')[0], '%Y-%m-%d').date()
        except Exception as e:
            print(f"Erro ao carregar estatísticas: {e}")
            total_pacientes = total_hc = total_pr = total_pd = 0
            pacientes_recentes = []
            
        return render_template('index.html', 
                               db_status=db_status, 
                               db_type=db_type,
                               total_pacientes=total_pacientes,
                               total_hc=total_hc,
                               total_pr=total_pr,
                               total_pd=total_pd,
                               pacientes_recentes=pacientes_recentes)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('base.html', page_title="Acesso Negado"), 403

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
