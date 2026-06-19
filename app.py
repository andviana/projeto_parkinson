from flask import Flask, render_template
from flask_login import LoginManager
from config import Config

# Inicialização global do Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        from services import auth_service
        return auth_service.load_user(user_id)
    except Exception as e:
        print(f"Erro ao carregar usuário no factory: {e}")
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa plugins
    login_manager.init_app(app)

    # Registro de Blueprints
    from blueprints.dashboard import dashboard_bp
    from blueprints.auth import auth_bp
    from blueprints.grupos import grupos_bp
    from blueprints.pacientes import pacientes_bp
    from blueprints.exames import exames_bp
    from blueprints.clinical_data import clinical_data_bp
    from blueprints.complementary_data import complementary_data_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(grupos_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(exames_bp)
    app.register_blueprint(clinical_data_bp)
    app.register_blueprint(complementary_data_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('base.html', page_title="Acesso Negado"), 403

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
