from backup import Backup

b = Backup()

def daily(name):
    """Make a daily backup of a directory."""
    b.backup(name,'daily')

def weekly(name):
    """Make a weekly backup of a directory."""
    b.backup(name,'weekly')
