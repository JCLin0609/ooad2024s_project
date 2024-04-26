from flask import render_template, Blueprint, request, redirect, flash, url_for
from app.services import afl_service

bp = Blueprint('afl_controller', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    file = request.files['file']
    duration = request.form.get('duration')
    if file:
        result = aflService.uploadFuzzTarget(file, duration)
        if result:
            flash(f'{file.filename} 上傳成功 (Run for {duration} hrs)')
        else:
            flash(f'{file.filename} 上傳失敗 (Run for {duration} hrs)')
    return redirect(url_for('afl_controller.upload'))


@bp.route('/observe', methods=['GET', 'POST'])
def observe():
    if request.method == 'GET':
        targetNames = aflService.observeFuzzTarget()
        currentTargetName = aflService.current_target.name if aflService.current_target else None
        return render_template('observe.html', targetNames=targetNames, currentTargetName=currentTargetName)


@bp.route('/execute', methods=['POST'])
def execute():
    targetName = request.form.get('targetName')
    aflService.startRunningTarget(targetName)
    return redirect(url_for('afl_controller.observe'))


aflService = afl_service.FuzzService()
