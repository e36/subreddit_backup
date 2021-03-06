from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import praw
import OAuth2Util
from reddit import get_post_data, get_posts, get_comments
from database import insert_comment_data, insert_history, insert_post_data, get_post_data_from_db
from database import check_post_table, check_comment_table, get_comment_keys, bulk_comment_insert
from datetime import datetime
from redishandler import RedisHandler
import redis
import time


class SessionHandler:

    def __init__(self, databasesettings, settings, redissettings, dbonly=False):

        # grab config settings
        self.settings = settings
        self.dbsettings = databasesettings
        self.rsettings = redissettings

        # other state settings to worry about
        self.isrunning = False  # used to start or stop the backend

        # connect to database engine
        self.engine = self.connect_to_db()

        # create a sql alchemy session
        self.Session = sessionmaker(bind=self.engine)

        # connect to redis instance
        self.redis = RedisHandler(self.rsettings)

        # create praw instance, but only if dbonly is False
        # init praw and OAuth2Util things
        if not dbonly:
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
        connection_string = dbsettings['engine'] + "+mysqlconnector://" + dbsettings['username'] + ":" + dbsettings['password'] + "@" + dbsettings['hostname'] + ":" + dbsettings['port'] + "/" + dbsettings['dbname'] + "?charset=utf8mb4"

        # create engine object
        engine = create_engine(connection_string)

        return engine
    
    def start(self):
        """
        Runs the bot
        :return: nothing at all
        """

        print("Starting the backup process.")

        # refresh oauth tokens
        self.o.refresh()

        # check queue size before grabbing any more
        queueitems = self.redis.get_list_size()

        # if there aren't any items already in the queue, then get them
        if not queueitems:
            print('Getting thread IDs from reddit.\n')

            # get all available threads via praw
            threads = get_posts(self.r, self.settings['defaultsubreddit'])

            # only add to the redis queue if something is returned
            if threads:
                self.redis.add_to_queue(threads)

        # get the queue size one more time
        queueitems = self.redis.get_list_size()

        # run this until the queue is empty
        while queueitems:

            # get the next thread from the queue
            nexitem = self.redis.get_next()


            try:
                # work the thread
                self.grab_data(nexitem)

            except praw.errors.HTTPException:
                # This is meant to catch timeouts for when reddit is down or unresponsive

                print('HTTPException! Reddit must be down.')
                print('Waiting 2 minutes before continuing.\n')

                # push the thread id back onto the front of the queue
                self.redis.lpush(nexitem)

                # sleep for a bit
                time.sleep(120)

                continue

            # except:
                # TypeError: getresponse() got an unexpected keyword argument 'buffering'

                # print("TypeError!  I don't know what the fuck this is, so we're gonna reset and try again.\n")

                # push the current item back into the queue
                # self.redis.lpush(nexitem)

                # time.sleep(60)

                # continue



        print('Done.')



    def grab_data(self, thread_id):
        """
        Gets posts, inserts/updates the database, inserts history entry
        :return: nothing
        """

        # threads = ['42e77i']

        # init skip variable, should be false by default
        skip = False

        # empty tblHistory dict
        history = dict()

        # get created datetime for tblHistory
        history['created'] = datetime.utcnow()

        # make sure oauth tokens are good, since grabbing threads can take a while
        self.o.refresh()

        # get post data from reddit
        retdata = get_post_data(self.r, thread_id)

        # get post data from database
        # dbdata = get_post_data_from_db(self.Session, thread)

        # package the data for skip_logic
        # package = dict()
        # package['reddit'] = dict(thread_id=retdata['id'], comments=retdata['comments'], archived=retdata['archived'])
        # package['database'] = dbdata

        # if the database doesn't contain a record for the post, it will return false
        # if that happens then we don't want to run it through the skip logic

        # get comments for post from reddit
        data = get_comments(self.r, thread_id)

        # if data['status'] == 'C' then the retrieval was successful, so proceed
        if data['status'] == 'C':

            # query the database to see if the post already exists, will either get ID or None
            post_id = check_post_table(self.Session, thread_id)

            # if the post does not exist (no id returned) then insert the post data into db
            # you can do bulk_comment_insert on everything because this is all new data
            if not post_id:
                post_id = insert_post_data(self.Session, retdata)
                bulk_comment_insert(self.Session, data['comments'], post_id)
            else:
                # go through all comments and insert into database
                for comment in data['comments']:
                    insert_comment_data(self.Session, comment, post_id)

            # get finished time for tblHistory
            history['finished'] = datetime.utcnow()

            # build tblhistory entry
            history['message'] = 'Fetched post ID {0} with {1} comments'.format(retdata['id'], len(data['comments']))
            print(history['message'])

            # set status for now, until I'm able to implement error handling
            history['status'] = 'C'

        elif data['status'] == 'F':
            # data['status'] == 'F' so we build the message and send to insert_history
            history = dict(
                status=data['status'],
                finished=datetime.utcnow(),
                message=data['thread'] + ' failed due to ' + data['errormsg']
            )

        # insert message
        insert_history(self.Session, history)

        print("\n")

    def get_reddit_post(self, thread_id):
        """
        Gets the reddit post by thread id
        :param thread_id: thread is (e.g. '4108ez')
        :return: nothing
        """

        pass

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

    def check_post_table(self, thread_id):
        """
        Checks the table for a post
        :param thread_id: thread id (e.g. 'cghs2')
        :return: db ID or None
        """

        # print("Searching db for " + thread_id)

        a = check_post_table(self.Session, thread_id)

        # print("Result {0}".format(a))

    def check_comment_table(self, comment_id):
        """
        Checks the table for a post
        :param comment_id: thread id (e.g. 't1_s72x7')
        :return: db ID or None
        """

        print("Searching db for " + comment_id)

        a = check_comment_table(self.Session, comment_id)

        print("Result {0}".format(a))

    def get_comment_keys(self, thread_id):

        retlist = []

        retlist = get_comment_keys(self.Session, thread_id)

        return retlist

