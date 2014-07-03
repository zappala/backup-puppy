from backup import Backup

b = Backup()

def daily():
    """Do all daily backups."""
    b.backup_all('daily')

def weekly(name):
    """Do all weekly backups."""
    b.backup_all('weekly')
