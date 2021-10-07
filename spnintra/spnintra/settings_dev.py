#開発環境固有の設定ファイル
from.settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#メディアファイル
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#　ロギング設定
LOGGING = {
    'version': 1, #1固定
    'disable_existing_loggers': False,

    #ロガーの設定
    'loggers':{
        #Djangoが利用するロガー
        'django':{
            'handlers':['console'],
            'level': 'INFO',
        },
        #アプリケーションが利用するロガー
        'infomation': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'overview': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'schedule': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'timecard': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'directory': {
            'handlers':['console'],
            'level': 'DEBUG',
        },
        'report': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'workflow': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'infoboard': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'message': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'task': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'equipment': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'employee': {
            'handlers':['console'],
            'level': 'DEBUG',
        },
        'employeeinfo': {
            'handlers':['console'],
            'level': 'DEBUG',
        },
        'rpa': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'syssetting': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },

    #ハンドラの設定
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'dev'
        },
    },

    #フォーマッタの設定
    'formatters':{
        'dev':{
            'format':'\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}