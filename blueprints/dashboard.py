from flask import Blueprint, render_template, abort
from flask_login import login_required
from services import dashboard_service

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    try:
        data = dashboard_service.get_dashboard_data()
        return render_template('index.html', **data), 200
    except Exception as e:
        print(f"Erro ao processar dashboard: {e}")
        abort(500)
