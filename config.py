import os

basedir = os.path.abspath(os.path.dirname(__file__))  # ????/


class Config:
    SECRET_KEY = 'gggjklsdjflsdjkf'  # 提交表单的时候有一个秘钥，可以防止CSRF攻击

    FLASKY_MAIL_SUBJECT_PREFIX = 'Flasky Register'  # 邮件的主题
    MAIL_SERVER = 'smtp.qq.com'  # 邮件相关配置
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '419259833@qq.com'
    MAIL_PASSWORD = 'zcdphnwmtzuobhii'
    MAIL_SENDER = '419259833@qq.com'
    FLASK_MAIL_ADMIN = '419259833@qq.com'
    FLASK_ADMIN = '419259833@qq.com'

    FLASKY_FOLLOWERS_PER_PAGE = 20
    FLASKY_COMMENTS_PER_PAGE = 20
    FLASKY_POSTS_PER_PAGE = 20

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 数据库这个一定要写
    SQLALCHEMY_RECORD_QUERIES = True  # 数据库缓慢查询配置
    FLASK_SLOW_DB_QUERY_TIME = 0.5

    CACHE_TYPE = 'simple'  # 缓存设置

    CKEDITOR_SERVE_LOCAL = True  # 富文本


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # 关闭这个防止Flask-DEBUGToolbar每次都重定向
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TsetingCongig(Config):
    TESTING = True  # 开启调试模式
    WTF_CSRF_ENABLED = False  # 测试模式关闭csrf
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    FLASK_DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1332931844@localhost/flask'


config = {
    'development': DevelopmentConfig,
    'testing': TsetingCongig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


