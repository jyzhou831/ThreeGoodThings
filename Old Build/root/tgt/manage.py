#!/home/logicalrealist/env/bin/python

import sys, os
sys.path.append(os.getcwd())
sys.path.insert(0,'/home/logicalrealist/env/bin')
sys.path.insert(0,'/home/logicalrealist/env/lib/python2.5/site-packages/Django-1.3-py2.5.egg')
sys.path.insert(0,'/home/logicalrealist/env/lib/python2.5/site-packages')
sys.path.insert(0,'/home/logicalrealist/threegoodthings.net/tgt')

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
