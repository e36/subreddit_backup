from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models_mysql import Subreddit, Post, Comment, Message, MessageLog


class Bot:

    def __init__(self, databasesettings):

        self.settings = databasesettings
        print(self.settings['engine'])

        # figure out what kind of database engine we're using
        # TODO: figure out how to support different database engines

        # connect to database engine
        self.engine = self.connect_to_db()

        # create a session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def connect_to_db(self):

        """
        Connects to a database.
        :param dbsettings: a configparser dict with all necessary connection information
        :return: a sqlalchemy.engine object
        """

        # grab database settings
        dbsettings = self.settings

        # build connection string
        # engine://user:pass@host/database
        connection_string = dbsettings['engine'] + "://" + dbsettings['username'] + ":" + dbsettings['password'] + "@" + dbsettings['hostname'] + ":" + dbsettings['port'] + "/" + dbsettings['dbname']
        print(connection_string)

        # create engine object
        engine = create_engine(connection_string)

        return engine

    def check_messages(self):
        """
        Check the messages table
        :return: nothing?
        """

        # get next message in tblMessages
        result = self.session.query(Message).first()

        # process message
        if result:
            execute = datetime.utcnow()
            print("MESSAGE: " + result.message + " RECEIVED " + str(result.created) + "\n")
        else:
            print("No messages\n")

        # move message to tblMessageLog
        if result:
            message = MessageLog(message=result.message, created=result.created, executed=execute)
            self.session.add(message)
            self.session.delete(result)
            self.session.commit()

    def process_message(self, message):
        """
        Processes a database message
        :param message: a database message
        :return: nothing?
        """

        # the types of messages currently supported
        message_types = ['GET']

        # most messages are going to be something like "GET <thread id" so we split it to make it easier to process
        message_split = message.split()

        # do any of the components match message_types? THIS ASSUMES TWO WORD MESSAGES FOR NOW
        for element in message_split:
            if element in message_types:
                message_command = element
            else:
                message_target = element

