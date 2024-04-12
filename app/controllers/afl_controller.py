from flask import render_template
from flask import Blueprint
from app.services import afl_service

bp = Blueprint('afl_controller',__name__)
    
@bp.route('/')
def index():
    users = aflService.users()
    return render_template('index.html', users=users)

@bp.route('/upload')
def upload():
    return render_template('UploadPage.html')

aflService = afl_service.FuzzService()