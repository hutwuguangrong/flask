
import os
import logging
import click
from flask import Flask, current_app

from flask_migrate import upgrade, Migrate
from flask_sqlalchemy import get_debug_queries
from logging.handlers import RotatingFileHandler, SMTPHandler

from config import config, basedir
from app.extensions import bootstrap, moment, db, login_manager, mail, toolbar, cache, ckeditor
from app.faker import fake_users, fake_posts
from app.models import Role, User, Post


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)  # flask的应用实例，所有的客户端请求都是这个实例处理
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)

    migrate = Migrate(app, db)

    return app


def register_logging(app):

    app.logger.setLevel(logging.INFO)  # 将app.logger等级设为INFO等级
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 日志的输出格式

    file_handler = RotatingFileHandler(os.path.join(basedir, 'blog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)  # 防止日志日积月累产生一个巨大的日志文件配置

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)  # 将接受的日志等级设为INFO

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_errors(app):
    pass


def register_template_context(app):
    pass


def register_blueprints(app):
    from app.api import api as api_blueprint
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # pre表示这个蓝本的所有路由都会加上这个前缀
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')


def register_shell_context(app):
    @app.shell_context_processor  # 要想进入shell时将对象自动导入列表中，必须用这个装饰器，注册一个shell上下文处理器
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Post=Post)


def register_commands(app):
    @app.cli.command()
    def test():
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)

    @app.cli.command()
    @click.option('--users', default=100, help='Quantity of messages, default is 100.')
    @click.option('--posts', default=100, help='Quantity of messages, default is 100.')
    def forge(users=100, posts=100):
        # flask forge --users=100 --posts=100
        click.echo('Working.....')
        fake_users(users)
        fake_posts(posts)
        db.session.commit()
        click.echo('Create {} fake users, {} fake posts.'.format(users, posts))

    @app.cli.command()
    def deploy():
        # 把数据库迁移到最新修订版本
        upgrade()

        # 用户角色 创建或更新
        Role.insert_roles()

        # 确保所有的用户都关注了自己
        User.add_self_follows()


def register_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
    cache.init_app(app)
    ckeditor.init_app(app)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for query in get_debug_queries():
            if query.duration >= app.config['FLASK_SLOW_DB_QUERY_TIME']:
                current_app.logger.warning(
                    'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                    % (query.statement, query.parameters, query.duration, query.context)
                )
        return response