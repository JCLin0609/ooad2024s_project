from flask import render_template, Blueprint, request, redirect, flash, url_for, Response, stream_with_context
from app.services.afl_service import AFLService
from app.services.report_service import ReportService
from app.services.upload_service import UploadService
from app.Repository.fuzz_target_repository import FuzzTargetRepository

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
        result = uploadService.upload_fuzz_Target(file)
        if result:
            flash(f'{file.filename} 上傳成功 (Run for {duration} hrs)')
        else:
            flash(f'{file.filename} 上傳失敗 (Run for {duration} hrs)')
    return redirect(url_for('afl_controller.upload'))


@bp.route('/observe', methods=['GET', 'POST'])
def observe():
    return render_template('observe.html')


@bp.route('/reports', methods=['GET'])
def reports():
    targetNames = reportService.get_target_names()
    currentTargetName = aflService.current_running_target(
    ).name if aflService.current_running_target() else None
    return render_template('reports.html', targetNames=targetNames, currentTargetName=currentTargetName)


@bp.route('/reports/<targetName>', methods=['GET'])
def report(targetName):
    target = fuzzTargetRepository.get(targetName)
    if target is None:
        return Response("Not Found", status=404)
    return render_template('targetReport.html', target=target)


@bp.route('/replay', methods=['GET'])
def replay():
    pass


@bp.route('/execute', methods=['POST'])
def execute():
    targetName = request.form.get('targetName')
    aflService.start_running_target(targetName)
    return redirect(url_for('afl_controller.observe'))


@bp.route('/stop', methods=['POST'])
def stop():
    aflService.stop_running_target()
    return redirect(url_for('afl_controller.observe'))


fuzzTargetRepository = FuzzTargetRepository()
aflService = AFLService(fuzzTargetRepository)
uploadService = UploadService(fuzzTargetRepository)
reportService = ReportService(fuzzTargetRepository)
