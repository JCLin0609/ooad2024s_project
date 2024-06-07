from flask import render_template, Blueprint, request, redirect, flash, url_for, Response, stream_with_context
from app.services.afl_service import AFLService
from app.services.report_service import ReportService
from app.services.upload_service import UploadService
from app.services.replay_service import ReplayService
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
    target_names = reportService.get_target_names()
    current_target_name = aflService.current_running_target_name()
    return render_template('reports.html', targetNames=target_names, currentTargetName=current_target_name)


@bp.route('/reports/<targetName>', methods=['GET'])
def target_report(targetName):
    target_report = reportService.get_target_report(targetName)
    target_report_img_path = reportService.get_target_report_img_path(
        targetName)
    return render_template('target_report.html', target=targetName, targetResult=target_report, imgs=target_report_img_path)


@bp.route('/replay', methods=['GET'])
def replay():
    target_name = request.args.get('targetName')
    crash_num = request.args.get('crashNum')
    target_report_content = replayService.replay_target(
        target_name, crash_num)
    return render_template('replay.html', targetName=target_name, crash=crash_num, htmlContent=target_report_content)


@bp.route('/execute', methods=['POST'])
def execute():
    target_name = request.form.get('targetName')
    aflService.start_running_target(target_name)
    return redirect(url_for('afl_controller.observe'))


@bp.route('/delete', methods=['POST'])
def delete():
    delete_target_list = request.get_json()
    aflService.delete_target(delete_target_list)
    return redirect(url_for('afl_controller.reports'))


@bp.route('/stop', methods=['POST'])
def stop():
    aflService.stop_running_target()
    return redirect(url_for('afl_controller.reports'))


fuzzTargetRepository = FuzzTargetRepository()
aflService = AFLService(fuzzTargetRepository)
uploadService = UploadService(fuzzTargetRepository)
reportService = ReportService(fuzzTargetRepository)
replayService = ReplayService(fuzzTargetRepository)
