__author__ = 'e36'
__version__ = '0.6'

import praw
import time
import configparser
from sessionhandler import SessionHandler

# print intro
print('***Subreddit Backup Bot***')
print('version {0}'.format(__version__))

# get config data and save to global variables
config = configparser.ConfigParser()
config.read('config.dat')
DATABASE = config['database']
SETTINGS = config['settings']

# init praw stuff
r = praw.Reddit(user_agent='IAmA and Askreddit parsing script by u/e36')

# create bot, connect to database
backend = SessionHandler(DATABASE, SETTINGS)

# start the backend
backend.start()
