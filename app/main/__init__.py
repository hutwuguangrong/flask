from flask import Blueprint

from ..models import Permission

main = Blueprint('main', __name__)  # 注意这里要放在导入views前面

from . import views, errors, forms


@main.app_context_processor  # 为了避免每次调用render_template都多添加一个模板参数，可以使用上下文处理器，让变量在所有模板中都可以使用
def inject_permissions():
    return dict(Permission=Permission)