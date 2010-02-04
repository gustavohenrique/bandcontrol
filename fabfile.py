from fabric import *
import datetime

config.datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
config.source = '/home/usuario/www'
config.project = 'bandcontrol'
config.package_compress = '$(project).tar.gz'

config.destination = '/var/www/xsol/projects'

# Remote servers
config.fab_user = 'root'
config.fab_password = 'senhadoroot'
config.fab_hosts = ['192.168.0.1']

def deploy():
    # Remove os *.pyc
    local("find $(source)/$(project) -name '*.pyc' -delete")
    local("find $(source)/$(project) -name '*~' -delete")
    # Compacta
    local('cd $(source) && tar czvf /tmp/$(package_compress) $(project) --exclude=files --exclude-vcs')
    # Envia ao dir /tmp do servidor
    put('/tmp/$(package_compress)','/tmp')
    # Backup do dir do projeto no servidor
    run('tar czvf $(destination)/$(datetime).tar.gz $(destination)/$(project)')
    # Descompacta
    run('tar zxvf /tmp/$(package_compress) -C $(destination)')
    # syncdb
    run('cd $(destination)/$(project) && python manage.py syncdb')

