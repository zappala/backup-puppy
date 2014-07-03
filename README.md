# backup-puppy

Incremental backup using Python, fabric, and rsync

## Installation

Clone this repository:

```
git clone git@github.com:zappala/backup-puppy.git
```

Install a few things through apt:

```
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo pip install virtualenv
```

Create a virtual environment:

```
mkdir ~/virtualenvs
virtualenv ~/virtualenvs/backup-puppy
source ~/virtualenvs/backup-puppy/bin/activate
```

Install Python requirements:

```
cd backup-puppy
pip install -r requirements.txt
```

## Configuration

Create a backup directory:

```
sudo mkdir /home/backups
sudo chown user /home/backups
```

where 'user' is your user ID.

Create a configuration file:

```
cp doc/puppy.cfg /home/backups/puppy.cfg
```

Edit the configuration file to add your SMTP settings and add your backups.
The backup syntax is

```
backup name location
```

Where 'name' is a unique string and location is a local or remote directory,
such as user@example.com:/home/user/wiki.

Setup a cron job to do daily backups:

```
crontab -e
```

In this file, put the following:

```
SHELL=/bin/bash

0 1 * * * source $HOME/virtualenvs/backup-puppy/bin/activate && cd $HOME/backup\
-puppy && fab daily
0 2 * * 1 source $HOME/virtualenvs/backup-puppy/bin/activate && cd $HOME/backup\
-puppy && fab weekly
```

Note, to backup directories on remote machines, you will need to setup 
your SSH keys appropriately.

