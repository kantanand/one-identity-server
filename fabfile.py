from __future__ import with_statement
import os, time
from fabric.api import local, run, env, put, task, cd, sudo, settings, hide, prompt
from fabric.tasks import execute
from fabric.contrib.project import rsync_project
from fabric.utils import warn
import identityfabfile as identity

def apt_update():
	sudo('apt-get update')


def apt_get_install(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)

@task
def install_mysql():
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
        return
    mysql_password = prompt('Please enter MySQL root password:')
    sudo('echo "mysql-server-5.5 mysql-server/root_password password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.5 mysql-server/root_password_again password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    apt_get_install('mysql-server')

@task
def install_nginx():
    apt_get_install('nginx')

@task
def env():
    print('creating env')
    run('virtualenv env')


@task
def dependencies():
    apt_update()
    apt_get_install(
        'build-essential', 
        'autoconf',
        'libtool', 
        'pkg-config', 
        'rsync',
        'libffi-dev', 
        'libssl-dev', 
        'libmysqlclient-dev', 
        'python-virtualenv', 
        'python-dev', 
        'binutils', 
        'libproj-dev', 
        )

@task
def newsetup():
    execute(dependencies)
    execute(install_mysql)
    execute(install_nginx)
    execute(env)
