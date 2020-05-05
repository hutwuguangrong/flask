from flask_bootstrap import Bootstrap
from flask_caching import Cache

from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()  # 记得创建之后在create_app里面init
moment = Moment()  # 求本地时间的一个扩展
db = SQLAlchemy()  # db表示应用的数据库
mail = Mail()  # 邮件
login_manager = LoginManager()  # 登录模块实例
login_manager.login_view = 'auth.login'
# login_manager的login_view属性用来设置登录页面的端点，匿名用户尝试访问受保护的页面是将重定向到登录页面，因为是在蓝本中定义，所以还要加上蓝本的名字
pagedown = PageDown()  # 富文本
toolbar = DebugToolbarExtension()  # 一个dubug工具
cache = Cache()  # 设置缓存