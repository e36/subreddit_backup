from sqlalchemy import update
from datetime import datetime
from models_mysql import MessageLog, Message, Post, Subreddit, Comment


def get_message(session):
    """
    Gets the next message from tblMessages
    :param session: sql alchemy session
    :return: the message or None
    """
    print('Checking messages...')

    # get next message in tblMessages
    result = session.query(Message).first()

    # return message or None
    if result:
        return result
    else:
        return None


def move_message(session, messageid):
    """
    Moves a message from tblMessages to tblMessageLog
    :param session: sql alchemy session
    :param messageid: the message ID to be moved
    :return:
    """

    # move message to tblMessageLog
    # create db objects
    oldmessage = session.query(Message).filter_by(id=messageid).one()
    messagelog = MessageLog(message=oldmessage.message, created=oldmessage.created, executed=datetime.utcnow())

    # add message to MessageLog table, and delete from Message table
    session.add(messagelog)
    session.delete(oldmessage)

    # commit
    session.commit()


def check_subreddit_by_name(session, subreddit):
    """
    Checks tblSubreddits to see if the subreddit name exists.  If yes, then return the table ID.  If no, insert into
    table and return table ID.
    :param session: sql alchemy session object
    :param subreddit: subreddit name
    :return: subreddit ID from tblSubreddits
    """

    tablentry = session.query(Subreddit).filter_by(name=subreddit)

    if tablentry:
        return tablentry.id
    else:
        # it does not exist in the table, so insert and return the table id
        domain = 'self.' + subreddit
        sub = Subreddit(name=subreddit, domain=domain)
        session.add(sub)
        session.commit()
        return sub.id


def check_subreddit_by_domain(session, domain):
    """
    Checks tblSubreddits to see if the subreddit domain exists.  If yes, then return the table ID.  If no, insert into
    table and return the table ID.
    :param session: sql alchemy session
    :param domain: PRAW domain (e.g. 'self.IAmA')
    :return: table ID of the domain
    """

    tablentry = session.query(Subreddit).filter_by(domain=domain)

    if tablentry:
        return tablentry.id
    else:
        # it does not exist in the table, so insert and return the table id
        subname = domain.split(sep='.')
        sub = Subreddit(name=subname[0], domain=domain)
        session.add(sub)
        session.commit()
        return sub.id


def insert_post_data(session, post_data):
    """
    Inserts post data into tblPosts.  This will insert or update depending on whether the post already exists
    in the database or not.  It will skip the author if the author deleted the post since the last update.
    :param session: sql alchemy session
    :param post_data: dict with all post data
    :return:
    """

    #  first check to see if the post already exists in the database
    post = session.query(Post).filter_by(thread_id=post_data['thread_id']).one()
