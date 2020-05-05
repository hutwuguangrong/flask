from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(404)  # 定义为mian.errorhandler只有在main蓝本中才能触发这个错误
def page_not_found(e):  # 根据accept的请求首部响应不同的格式
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500