from flask import render_template
from flask import Blueprint
from flask import request
from flask import current_app
from app.services import afl_service
import os

bp = Blueprint('afl_controller',__name__)
    
@bp.route('/')
def index():
    users = aflService.users()
    return render_template('index.html', users=users)

@bp.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            return '上傳成功'
        return '上傳失敗'
    return render_template('UploadPage.html')

aflService = afl_service.FuzzService()