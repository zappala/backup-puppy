import os

from fabric.api import local, run, settings

from config import Config

c = Config()

def daily(name):
    """Make a daily backup of a directory."""
    location = "%s/%s" % (c.location,name)
    directory = c.backups[name]['directory']
    number = c.backups[name]['daily']
    # make directories
    c.makedirs(name)
    # setup link to previous backup
    link = ""
    if os.path.exists('%s/backup.daily.1' % (location)):
        link = "--link-dest=../backup.dailyt.1"
    # make new backup
    with settings(warn_only=True):
        op = local("rsync -a --delete %s %s %s/backup.daily.0" % (link,directory,location),capture=True)
    if op.failed:
        c.send_email(name,'daily',op.stderr)
    else:
        # rotate backups
        c.rotate(name,'daily')
