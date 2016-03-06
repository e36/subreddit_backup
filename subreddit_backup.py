import configparser
from sessionhandler import SessionHandler

# print intro
print('***Subreddit Backup, by e36***')

# get config data and save to global variables
config = configparser.ConfigParser()
config.read('config.dat')
DATABASE = config['database']
SETTINGS = config['settings']
REDIS = config['redis']

# create bot, connect to database
backend = SessionHandler(DATABASE, SETTINGS, REDIS)

# start the backend
backend.start()
