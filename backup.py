import os

from fabric.api import local
from fabric.api import run

from config import Config

b = Config()
b.add(name='wiki',directory='zappala@internet.byu.edu:/home/zappala/dokuwiki')

def daily(name):
    """Make a daily backup of a directory."""
    location = "%s/%s" % (b.location,name)
    directory = b.backups[name]['directory']
    number = b.backups[name]['daily']
    # make directories
    b.makedirs(name)
    # make new backup
    ## TBD: check for success and email on failure
    if os.path.exists('%s/backup.daily.1' % (location)):
        o = local("rsync -a --delete --link-dest=../backup.daily.1 %s %s/backup.daily.0" % (directory,location))
    else:
        o = local("rsync -a --delete %s %s/backup.daily.0" % (directory,location))
    # rotate backups
    b.rotate(name,'daily')
