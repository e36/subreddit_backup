__author__ = 'e36'
__version__ = '0.6'

import praw
import time
import configparser
from database import connect_to_db
import sqlalchemy

# print intro
print('***Subreddit Backup Bot***')
print('version {0}'.format(__version__))

# get config data and save to global variables
config = configparser.ConfigParser()
config.read('config.dat')
DATABASE = config['database']
SETTINGS = config['settings']

# init praw stuff
r = praw.Reddit(user_agent='backup script by /u/e36')

# connect to the database
db = connect_to_db(DATABASE)

# main loop
while True:
    print("bot")
    time.sleep(5)
