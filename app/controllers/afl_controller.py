from flask import render_template
from flask import Blueprint
from app.services import afl_service

bp = Blueprint('afl_controller',__name__)

@bp.route('/')
def index():
    users = afl_service.users()
    return render_template('index.html', users=users)