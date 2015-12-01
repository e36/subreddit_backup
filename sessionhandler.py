from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import praw
import OAuth2Util
from reddit import get_post_data, get_posts, get_comments
from database import insert_comment_data, insert_history, insert_post_data, get_thread_skip_data_db
from datetime import datetime


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
        # init praw and OAuth2Util things
        self.r = praw.Reddit(user_agent='Subreddit parsing script by u/e36')
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.o.refresh()

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

        print("Starting the backup process.")
        self.grab_data()

    def grab_data(self):
        """
        Gets posts, inserts/updates the database, inserts history entry
        :return: nothing
        """

        # refresh oauth tokens
        self.o.refresh()

        # get all available threads via praw
        threads = []
        threads = get_posts(self.r, self.settings['defaultsubreddit'])

        for thread in threads:
            # iterate through thread IDs, and grab data

            # init skip variable, should be false by default
            skip = False

            # empty tblHistory dict
            history = dict()

            # get created datetime for tblHistory
            history['created'] = datetime.utcnow()

            # make sure oauth tokens are good, since grabbing threads can take a while
            self.o.refresh()

            # get post data from reddit
            retdata = get_post_data(self.r, thread)

            # get post data from database
            dbdata = get_thread_skip_data_db(self.Session, thread)

            # package the data for skip_logic
            package = dict()
            package['reddit'] = dict(thread_id=retdata['id'], num_comments=retdata['num_comments'], archived=retdata['archived'])
            package['database'] = dbdata

            # if the database doesn't contain a record for the post, it will return false
            # if that happens then we don't want to run it through the skip logic
            if hasattr(dbdata, 'thread_id'):
                # run through the skip logic
                skip = self.skip_logic(package)

            # see if the post exists in the database already
            if not skip:
                # don't skip the post

                # get comments
                comments = []
                comments = get_comments(self.r, thread)

                # insert into database
                post_id = insert_post_data(self.Session, retdata)

                # go through all comments and insert into database
                for comment in comments:
                    insert_comment_data(self.Session, comment, post_id)

                # get finished time for tblHistory
                history['finished'] = datetime.utcnow()

                # build tblhistory entry
                history['message'] = 'Fetched post ID {0} with {1} comments'.format(retdata['id'], len(comments))
                print(history['message'])

                # set status for now, until I'm able to implement error handling
                history['status'] = 'C'

                # create history message and isnert
                insert_history(self.Session, history)

                # just throw in a line return to space things out
                print('\n')
            else:
                # the thread is being skipped
                print('skipping thread {0}'.format(retdata['thread_data']['id']))

                # build tblhistory message
                status = 'S'
                finished = datetime.utcnow()
                message = 'Skipped post {0}'.format(retdata['id'])
                history = dict(status=status, finished=finished, message=message)

                # insert message
                insert_history(self.Session, history)

    def skip_logic(self, package):
        """
        All of the logic to decide whether a thread should be skipped.
        :param package: EITHER 0 or a dict('reddit','database') to signify sources.  Within each key there is
                        a dict('thread_id', 'num_comments', 'lastchecked', 'archived')
        :return: True (the post is good and should not be skipped) or False (the post should be skipped)
        """

        print('rd {0}'.format(package['reddit']['num_comments']))
        print('db {0}'.format(package['database']['num_comments']))

        if package['database']['num_comments'] == package['reddit']['num_comments']:
            return True
        else:
            return False

