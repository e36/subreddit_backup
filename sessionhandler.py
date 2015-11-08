from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
from reddit import get_post_data, get_posts
import praw
from database import insert_comment_data, insert_history, insert_post_data


class SessionHandler:

    def __init__(self, databasesettings, settings):

        # grab config settings
        self.settings = settings
        self.dbsettings = databasesettings

        # other state settings to worry about
        self.isrunning = False  # used to start or stop the backend

        # connect to database engine
        self.engine = self.connect_to_db()

        # create a sql alchemy session
        self.Session = sessionmaker(bind=self.engine)

        # create praw instance
        # init praw stuff
        self.r = praw.Reddit(user_agent='IAmA and Askreddit parsing script by u/e36')

    def connect_to_db(self):

        """
        Connects to a database.
        :param dbsettings: a configparser dict with all necessary connection information
        :return: a sqlalchemy.engine object
        """

        # grab database settings
        dbsettings = self.dbsettings

        # build connection string
        # engine://user:pass@host/database
        connection_string = dbsettings['engine'] + "://" + dbsettings['username'] + ":" + dbsettings['password'] + "@" + dbsettings['hostname'] + ":" + dbsettings['port'] + "/" + dbsettings['dbname'] + "?charset=utf8"

        # create engine object
        engine = create_engine(connection_string)

        return engine
    
    def start(self):
        """
        Runs the bot
        :return: nothing at all
        """

        print("Starting the back process.")
        self.grab_data()

    def grab_data(self):
        """
        Gets posts, inserts/updates the database, inserts history entry
        :return: nothing
        """

        threads = []
        threads = get_posts(self.r, self.settings['defaultsubreddit'])

        for thread in threads:
            # iterate through thread IDs, and grab data

            # get post data, including comments
            retdata = get_post_data(self.r, thread)

            # insert into database
            post_id = insert_post_data(self.Session, retdata['thread_data'])

            # go through all comments and insert into database
            for comment in retdata['comments']:
                insert_comment_data(self.Session, comment, post_id)

            # build tblhistory entry
            historymessage = 'Fetched post ID {0} with {1} comments'.format(retdata['thread_data']['id'], len(retdata['comments']))
            print(historymessage)

            # create history message and isnert
            insert_history(self.Session, historymessage)

            # just throw in a line return to space things out
            print('\n')