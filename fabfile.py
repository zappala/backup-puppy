from backup import Backup

b = Backup()

def daily():
    """Do all daily backups."""
    b.backup_all('daily')

def weekly():
    """Do all weekly backups."""
    b.backup_all('weekly')
