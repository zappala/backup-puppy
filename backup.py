import os
import shutil
import smtplib
from email.mime.text import MIMEText

from fabric.api import local, run, settings

class Backup(object):
    def __init__(self,filename='/home/backups/puppy.cfg'):
        self.backups = {}
        self.parse_config(filename)

    def parse_config(self,filename):
        with open(filename,'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    pass
                parts = line.split()
                if len(parts) < 2:
                    continue
                if parts[0] == 'backup':
                    self.add(parts[1],parts[2])
                    continue
                object.__setattr__(self, parts[0], parts[1])

    def add(self,name=None,directory=None,daily=7,weekly=4):
        if not name or not directory:
            return
        self.backups[name] = {'directory':directory,'daily':daily,
                              'weekly':weekly}

    def makedirs(self,name):
        location = "%s/%s" % (self.location,name)
        if not os.path.exists(location):
            os.makedirs(location)


    def backup(self,name,kind):
        location = "%s/%s" % (self.location,name)
        directory = self.backups[name]['directory']
        # make directories
        self.makedirs(name)
        # setup link to previous backup
        link = ""
        if os.path.exists('%s/backup.daily.1' % (location)):
            link = "--link-dest=../backup.daily.1"
        # make new backup
        with settings(warn_only=True):
            op = local("rsync -a --delete %s %s %s/backup.%s.0" % (link,directory,location,kind),capture=True)
        if op.failed:
            self.send_email(name,kind,op.stderr)
        else:
            # rotate backups
            self.rotate(name,kind)

    def rotate(self,name,kind):
        location = "%s/%s" % (self.location,name)
        number = self.backups[name][kind]
        if os.path.exists("%s/backup.%s.%d" % (location,kind,number)):
            shutil.rmtree("%s/backup.%s.%d" % (location,kind,number))
        for i in range(number-1,-1,-1):
            if os.path.exists("%s/backup.%s.%d" % (location,kind,i)):
                os.rename("%s/backup.%s.%d" % (location,kind,i),"%s/backup.%s.%d" % (location,kind,i+1))

    def send_email(self,name,kind,error):
        msg = MIMEText("Error message:\n\n" + error)
        msg['Subject'] = 'Backup Puppy: %s backup failure for %s' % (kind,name)
        msg['From'] = self.mail_from
        msg['To'] = self.mail_to

        s = smtplib.SMTP(self.mail_host,self.mail_port)
        s.login(self.mail_user,self.mail_password)
        s.sendmail(self.mail_from,[self.mail_to],msg.as_string())
        s.quit()
