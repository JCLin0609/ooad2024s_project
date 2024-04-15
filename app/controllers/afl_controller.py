from flask import render_template, Blueprint, request, redirect, flash, url_for
from app.services import afl_service

bp = Blueprint('afl_controller', __name__)


@bp.route('/')
def index():
    users = aflService.users()
    return render_template('index.html', users=users)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('UploadPage.html')

    file = request.files['file']
    if file:
        print(f'Uploading file: {file.filename}')
        result = aflService.uploadFuzzTarget(file)
        if result:
            flash(f'{file.filename} 上傳成功')
        else:
            flash(f'{file.filename} 上傳失敗')
    return redirect(url_for('afl_controller.upload'))


aflService = afl_service.FuzzService()
