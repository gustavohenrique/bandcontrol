# coding: utf-8
import django.conf.global_settings as DEFAULT_SETTINGS
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Django settings for teste project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gustavo Henrique', 'eu@gustavohenrique.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT_PATH, 'database.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
os.path.join(PROJECT_ROOT_PATH, 'static'),
)

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'e3q@fkw*llxj*u&amp;s)^96@!1qm6mf*x-p_n_%@m&amp;69_y2z^rva('

TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
# Uncomment the next line for simple clickjacking protection:
# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bandcontrol.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_admin_bootstrapped',

    'django.contrib.admin',
    'rede',
    'cliente',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

"""
Configuração do sudo

Sudo é um software que permite um usuário executar comandos como root.
É preciso adicionar o usuário que está executando o servidor web no
arquivo /etc/sudoers e definir os comandos que ele pode executar como
root.
Abaixo um exemplo de como configurar o /etc/sudoers

# usuário www-data pode executar qualquer comando como root sem senha
www-data  ALL=(ALL) NOPASSWD: ALL

# usuário www-data pode executar apenas os comandos iptables, arp e ping
Cmnd_Alias COMANDOS = /usr/sbin/iptables, /usr/sbin/arp, /usr/bin/ping
www-data  ALL=(ALL) NOPASSWD: COMANDOS
"""

# Diretorio contendo os scripts de controle de banda e firewall
SHELL_SCRIPT_DIR = os.path.join(PROJECT_ROOT_PATH, 'scripts')

# Caminho para o arquivo texto
FIREWALL_TXT_FILE = '%s/pontosderede.txt' % SHELL_SCRIPT_DIR

# Firewall
FIREWALL_SCRIPT = '%s/firewall' % SHELL_SCRIPT_DIR

# ARP para listar IPs conectados
ARP_COMMAND = '/sbin/arp -n | grep -iv incomplet | grep -iv address | grep -iv eth0 | sort'

