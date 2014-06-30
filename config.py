import os

class Config:
    def __init__(self):
        self.backups = {}
        self.location = "/home/backups"

    def set_location(self,directory):
        self.location = directory

    def add(self,name=None,directory=None,daily=7,weekly=4):
        if not name or not directory:
            return
        self.backups[name] = {'directory':directory,'daily':daily,
                              'weekly':weekly}

    def makedirs(self,name):
        location = "%s/%s" % (self.location,name)
        if not os.path.exists(location):
            os.makedirs(location)

    def rotate(self,name,kind):
        location = "%s/%s" % (self.location,name)
        number = self.backups[name][kind]
        if os.path.isfile("%s/backup.%s.%d" % (location,kind,number)):
            os.path.remove("%s/backup.%s.%d" % (location,kind,number))
        for i in range(number-1,-1,-1):
            if os.path.exists("%s/backup.%s.%d" % (location,kind,i)):
                os.rename("%s/backup.%s.%d" % (location,kind,i),"%s/backup.%s.%d" % (location,kind,i+1))

