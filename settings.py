# -*- coding: utf-8 -*-
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
JOIN = os.path.join


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gustavo Henrique', 'gustavo@gustavohenrique.net'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = JOIN(PROJECT_ROOT_PATH, 'database.db')
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = JOIN(PROJECT_ROOT_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
SECRET_KEY = 'alwto1ine4o@qjpe&e@6$@$i*wl+hixjumnh$^+$$3r(hhi53g'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'bandcontrol.urls'
TEMPLATE_DIRS = (
    JOIN(PROJECT_ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'rede',
    'cliente',
)

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
SHELL_SCRIPT_DIR = JOIN(PROJECT_ROOT_PATH, 'scripts')

# Caminho para o arquivo texto
FIREWALL_TXT_FILE = '%s/pontosderede.txt' % SHELL_SCRIPT_DIR

# Firewall
FIREWALL_SCRIPT = '%s/firewall' % SHELL_SCRIPT_DIR

# ARP para listar IPs conectados
ARP_COMMAND = '/usr/sbin/arp -n | grep -iv incomplet | grep -iv address | grep -iv eth0 | sort'

