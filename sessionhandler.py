from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time
import database


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
        connection_string = dbsettings['engine'] + "://" + dbsettings['username'] + ":" + dbsettings['password'] + "@" + dbsettings['hostname'] + ":" + dbsettings['port'] + "/" + dbsettings['dbname']
        print(connection_string)

        # create engine object
        engine = create_engine(connection_string)

        return engine
    
    def start(self):
        """
        Runs the bot
        :return: nothing at all
        """

        print("Starting the backend service.")

        while True:
            # this is a never-ending loop


            # look for messages
            self.check_messages()

            # sleep
            time.sleep(float(self.settings['sleepinterval']))

    def check_messages(self):
        """
        Check the messages table
        :return: nothing?
        """

        message = database.get_message(self.session)

        if message:

            # create db session
            session = self.Session()

            print('Message found! {} RECEIVED {}'.format(message.message, message.created))
            self.process_message(session, message)

            session.close()

    def process_message(self, session, message):
        """
        Processes a database message
        :param message: a database message
        :return: nothing?
        """

        # the types of messages currently supported
        message_types = ['GET']

        # most messages are going to be something like "GET <thread id" so we split it to make it easier to process
        #message_split = message.split()

        # do any of the components match message_types? THIS ASSUMES TWO WORD MESSAGES FOR NOW
        # TODO: Extend this to support multiple thread IDs

        messageid = message.id

        database.move_message(self.session, messageid)

