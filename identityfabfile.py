'''
Fabric script for UPLYF application setup
'''
import os

from fabric.api import cd, env, put, run, sudo, task, warn_only
from fabric.contrib.files import sed
from fabric.contrib.project import rsync_project
from fabric.tasks import execute

# ----------------------------------------------
# GLOBAL VARIABLES 
# ----------------------------------------------
repo_folder = os.path.dirname(os.path.abspath(__file__))
webserver = repo_folder + "/webserver"
database  = repo_folder + "/database"

db_host_name = "localhost"
db_user_name = "root"
db_user_pass = "root"

db_root_user_name = "root"
db_root_user_pass = "root"
db_root_host_name = "localhost"

env.identity_root = '/home/django/identity'
env.identity_home = '/home/django'

host_name = ""
domain_name = ""

if len(env.hosts) > 0:
    host_name = env.hosts[0].split('@')[-1]
    domain_name = host_name

if 'domain_name' in env:
    domain_name = env.domain_name
    host_name = domain_name
# ----------------------------------------------

# ----------------------------------------------
# STATIC VALUES TO BE SET 
# ----------------------------------------------
# DEBUG 
APP_DEBUG = 'False'
# APP SECRET 
SECRET_KEY = "syzg-=ovamkuuyx)y^zppfs$ps0l=53(c@)fz+d7yyg4)fc@27"
# SSL VERIFICATION 
PRODUCT_NAME = "Identity"
# DB: MYSQL
DB_ENGINE = "django.db.backends.mysql"
DB_HOSTNAME = "localhost" # NOTE: may be different only for production 
DB_PORT = "3306" # NOTE: may be different only for production 
DB_NAME = "my_db" # NOTE: may be different only for production 
DB_USER_NAME = "myadmin" # NOTE: may be different only for production 
DB_USER_PASSWORD = "mypass" # NOTE: may be different only for production 
# ----------------------------------------------

# ----------------------------------------------
# DYNAMIC VALUES TO SET BASED ON SITE 
# ----------------------------------------------
# DEFAULT DOMAIN SETTINGS 
SERVER_PROTOCOL = "http"
SERVER_HOSTNAME = "localhost"
SERVER_PORT = "8000"
# ----------------------------------------------

@task
def check_path():
    print("your webserver path: %s " % (webserver))
    print("your database path: %s " % (database))

@task
def check_domain():
    print ("your domain_name is %s" %(domain_name))

# Check Server and Set DB Connection
if host_name == '13.126.74.188':
    db_user_name = "my_db"
    db_user_pass = "myadmin"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "rootusk"
    db_root_host_name = db_host_name
    # DEFAULT DOMAIN SETTINGS
    SERVER_PROTOCOL = "http"
    SERVER_HOSTNAME = "13.126.74.188"
    SERVER_PORT = "80"
else:
    db_user_name = "my_db"
    db_user_pass = "myadmin"
    db_host_name = "localhost"
    db_root_user_name = "root"
    db_root_user_pass = "rootusk"
    db_root_host_name = db_host_name
    # DEFAULT DOMAIN SETTINGS
    SERVER_PROTOCOL = "http"
    SERVER_HOSTNAME = "13.126.74.188"
    SERVER_PORT = "80"

# set-up uwsgi
@task
def uwsgi():
    run('mkdir -p /tmp/identity/etc/init.d')
    put(webserver+'/uwsgi/etc/init.d/identity-uwsgi.ini', '/tmp/identity/etc/init.d/')
    put(webserver+'/uwsgi/etc/init.d/identity-uwsgi.sh',
        '/tmp/identity/etc/init.d/', mirror_local_mode=True)
    run('sudo cp -r /tmp/identity/etc/init.d/* /etc/init.d/')
    run('sudo chmod 700 /etc/init.d/identity-uwsgi.sh')
    run('sudo chown %s:%s /etc/init.d/identity-uwsgi.*' %(env.user,env.user))


# set-up nginx
@task
def nginx():
    run('mkdir -p /tmp/identity')
    # put(webserver+'/certs/*', '/tmp/identity')
    run('mkdir -p /tmp/identity/etc/nginx/sites-enabled')
    put(webserver+'/nginx/etc/nginx/sites-enabled/default',
        '/tmp/identity/etc/nginx/sites-enabled/')
    sed('/tmp/identity/etc/nginx/sites-enabled/default',
        "\[SERVER_NAME\]", host_name, backup='')
    # run('sudo cp -r /tmp/identity/* /')
    run('sudo /etc/init.d/nginx restart')

# start uwsgi
@task
def start_uwsgi():
    with warn_only():
        sudo('/etc/init.d/identity-uwsgi.sh start')


# stop uwsgi
@task
def stop_uwsgi():
    with warn_only():
        sudo('/etc/init.d/identity-uwsgi.sh stop')

# restart uwsgi
@task
def restart():
    execute(stop_uwsgi)
    execute(start_uwsgi)

# first time for setting up db Note: all data will be lost
@task
def setupdb():
    run('mkdir -p /tmp/identity')
    put(database+'/setup_database.sql', '/tmp/identity')
    run('mysql -u'+db_root_user_name+' -p'+db_root_user_pass+' -h '+db_root_host_name+' < /tmp/identity/setup_database.sql')

# first time after database setup
@task
def initial_migration():
    with cd(env.identity_root):
        run('/home/django/env/bin/python manage.py makemigrations \
             --settings=identity.settings-production')

# used to migrate data center app alone
@task
def migrate_datacenter():
    with cd(env.identity_root):
        run('/home/django/env/bin/python manage.py migrate datacenter --settings=identity.settings-production')


# sync all db
@task
def dbsync():
    with cd(env.identity_root):
        run('/home/django/env/bin/python manage.py migrate --settings=identity.settings-production')

# create super user
@task
def create_super_user():
    with cd(env.identity_root):
        run('less cr_superuser.py | /home/django/env/bin/python\
         manage.py shell --settings=identity.settings-production')

# sync all identity and nfdb django files
@task
def cp():
    print('copying identity source')
    rsync_project(remote_dir='/home/django', local_dir='.', exclude=['env','.git','*.pyc'])

@task
def set_config_values():
    '''
    set config values
    '''
    sed('/home/django/identity/identity/settings-production.py',
        "\[SERVER_NAME\]", host_name, backup='')
    sed('/home/django/identity/identity/settings.py',
        "\[SERVER_NAME\]", host_name, backup='')
    # STATIC  VALUES  SETTINGS
    sed('/home/django/identity/config.py', r"\[APP_DEBUG\]", APP_DEBUG, backup='')
    sed('/home/django/identity/config.py', r"\[SECRET_KEY\]", SECRET_KEY, backup='')
    sed('/home/django/identity/config.py', r"\[PRODUCT_NAME\]", PRODUCT_NAME, backup='')
    sed('/home/django/identity/config.py', r"\[DB_ENGINE\]", DB_ENGINE, backup='')
    sed('/home/django/identity/config.py', r"\[DB_HOSTNAME\]", DB_HOSTNAME, backup='')
    sed('/home/django/identity/config.py', r"\[DB_PORT\]", DB_PORT, backup='')
    sed('/home/django/identity/config.py', r"\[DB_NAME\]", DB_NAME, backup='')
    sed('/home/django/identity/config.py', r"\[DB_USER_NAME\]", DB_USER_NAME, backup='')
    sed('/home/django/identity/config.py', r"\[DB_USER_PASSWORD\]", DB_USER_PASSWORD, backup='')
    # DYNAMIC VALUES  SETTINGS 
    sed('/home/django/identity/config.py', r"\[SERVER_PROTOCOL\]", SERVER_PROTOCOL, backup='')
    sed('/home/django/identity/config.py', r"\[SERVER_HOSTNAME\]", SERVER_HOSTNAME, backup='')
    sed('/home/django/identity/config.py', r"\[SERVER_PORT\]", SERVER_PORT, backup='')

@task
def create_base_folders():
    '''
    create base folders for project
    '''
    run('mkdir -p /home/django/identity/log')
    run('mkdir -p /home/django/identity/uploads')
    run('mkdir -p /home/django/identity/media/uploads')
    run('mkdir -p /home/django/media/uploads')
    run('mkdir -p /home/django/database')

@task
def install_requirements():
    '''
    install python packages 
    '''
    run('/home/django/env/bin/pip install\
     -r /home/django/identity/requirements.txt')


# collect all static files
@task
def static():
    with cd(env.identity_root):
        run('/home/django/env/bin/python\
         manage.py collectstatic -v0 --noinput \
         --settings=identity.settings-production')

# clear all code
@task
def clearcode():
    run('rm -rf /home/django/identity')


# clearn all static riles
@task
def clearstatic():
    run('rm -rf /home/django/static')


# clear all code and static files
@task
def clear():
    execute(clearcode)
    execute(clearstatic)


@task
def setup():
    '''
    set up task for new server
    '''
    execute(nginx)
    execute(uwsgi)
    execute(setupdb)
    execute(cp)
    execute(set_config_values)
    execute(create_base_folders)
    execute(install_requirements)
    execute(initial_migration)
    execute(dbsync)
    execute(static)
    execute(create_super_user)
    execute(start_uwsgi)

@task
def deploy():
    '''
    code can be deployed to production or testing servers
    fab identity.deploy -H username@domain_name
    '''
    execute(cp)
    execute(set_config_values)
    execute(create_base_folders)
    execute(install_requirements)
    execute(dbsync)
    execute(static)

@task
def clean_deploy():
    '''
    Used to give clean build but, its a time consuming process
    '''
    execute(clear)
    execute(setupdb)
    execute(deploy)
    execute(create_super_user)
    execute(restart)

@task
def quick_deploy():
    '''
    Used to Copy Apps and Static file and restart
    '''
    execute(cp)
    execute(set_config_values)
    execute(create_base_folders)
    execute(install_requirements)
    execute(static)
    execute(restart)

@task
def create_debug_file():
    '''
    used to touch and create the debug file 
    '''
    with cd(env.identity_root):
        run("touch lets_debug")

@task
def remove_debug_file():
    '''
    used to touch and remove the debug file 
    '''
    with cd(env.identity_root):
        run("rm lets_debug")


@task
def enable_debug_mode():
    '''
    used to enable debug mode 
    '''
    execute(create_debug_file)
    execute(restart)

@task
def disable_debug_mode():
    '''
    used to disable debug mode 
    '''
    execute(remove_debug_file)
    execute(restart)