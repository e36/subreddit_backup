from sqlalchemy import update, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.sql import select, insert, update
from datetime import datetime
from models_mysql import MessageLog, Message, Post, Subreddit, Comment, History


def insert_history(Session, message):
    """
    Inserts a message into tblHistory.
    :param Session: sqlalchemy Session object
    :param message: text message to be inserted into the table
    :return: nothing
    """

    # create session
    session = Session()

    newhistory = History(
        message=message,
        created=datetime.utcnow()
    )

    # add to session and commit
    session.add(newhistory)
    session.commit()


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


def check_subreddit_by_name(Session, subreddit):
    """
    Checks tblSubreddits to see if the subreddit name exists.  If yes, then return the table ID.  If no, insert into
    table and return table ID.
    :param Session: sql alchemy session object
    :param subreddit: subreddit name
    :return: subreddit ID from tblSubreddits
    """

    # create session
    session = Session()

    tablentry = session.query(Subreddit).filter(Subreddit.name == subreddit).first()

    if hasattr(tablentry, 'id'):
        return tablentry.id
    else:
        # it does not exist in the table, so insert and return the table id
        domain = 'self.' + subreddit
        sub = Subreddit(name=subreddit, domain=domain)
        session.add(sub)
        session.commit()
        return sub.id


def check_subreddit_by_domain(Session, domain):
    """
    Checks tblSubreddits to see if the subreddit domain exists.  If yes, then return the table ID.  If no, insert into
    table and return the table ID.
    :param session: sql alchemy session
    :param domain: PRAW domain (e.g. 'self.IAmA')
    :return: table ID of the domain
    """

    # create session
    session = Session()

    tablentry = session.query(Subreddit).filter(Subreddit.domain == domain).first()

    if hasattr(tablentry, 'id'):
        return tablentry.id
    else:
        # it does not exist in the table, so insert and return the table id
        subname = domain.split(sep='.')
        sub = Subreddit(name=subname[0], domain=domain)
        session.add(sub)
        session.commit()
        return sub.id


def insert_post_data(Session, post_data):
    """
    Inserts post data into tblPosts.  This will insert or update depending on whether the post already exists
    in the database or not.  It will skip the author if the author deleted the post since the last update.
    :param Session: sql alchemy session
    :param post_data: dict with all post data
    :return:
    """

    # get subreddit info
    domain = check_subreddit_by_domain(Session, post_data['domain'])

    # create new session
    session = Session()

    #  first check to see if the post already exists in the database
    post = session.query(Post).filter(Post.thread_id == post_data['id']).first()

    if hasattr(post, 'id'):
        # the post already exists in the database, so just update the information

        # update post data
        post.selftext = post_data['selftext']
        post.selftext_html = post_data['selftext_html']
        post.score = post_data['score']
        post.upvote_ratio = post_data['upvote_ratio']
        post.link_flair_text = post_data['link_flair_text']
        post.num_comments = post_data['num_comments']
        post.lastchecked = datetime.utcnow()
        post.lastmodified = datetime.utcnow()

        session.add(post)
        session.commit()

        # return the post id, just in case
        return post.id

    else:
        # the post doesn't exist, so let's drop it all in
        p = Post(
            thread_id=post_data['id'],
            created_utc=post_data['created_utc'],
            name=post_data['name'],
            title=post_data['title'],
            author=post_data['author'],
            domain=domain,
            score=post_data['score'],
            num_comments=post_data['num_comments'],
            link_flair_text=post_data['link_flair_text'],
            upvote_ratio=post_data['upvote_ratio'],
            permalink=post_data['permalink'],
            selftext=post_data['selftext'],
            selftext_html=post_data['selftext_html'],
            lastchecked=datetime.utcnow(),
            lastmodified=datetime.utcnow()
        )

        # add to session
        session.add(p)
        session.commit()

        return p.id


def insert_comment_data(Session, commentdata, post_id):
    """
    Inserts or updates one comment record.
    :param Session: sqlalchemy session
    :param commentdata: dict of comment data
    :param sub_id: subreddit id
    :return: row id
    """

    # create database session
    session = Session()

    # run query to see if the comment already exists
    comment = session.query(Comment).filter(Comment.id == commentdata['link_id']).first()

    if hasattr(comment, 'id'):
        # comment exists, so just update (don't update the author in case they delete
        comment.body = commentdata['body']
        comment.body_html = commentdata['body_html']
        comment.score = commentdata['score']
        comment.lastchecked = datetime.utcnow()
        comment.lastmodified = datetime.utcnow()

        # add to session and commit
        session.add(comment)
        session.commit()
    elif not hasattr(comment, 'id'):
        newcomment = Comment(
            link_id=post_id,
            name=commentdata['name'],
            parent_id=commentdata['parent_id'],
            score=commentdata['score'],
            created_utc=commentdata['created_utc'],
            author=commentdata['author'],
            body=commentdata['body'],
            body_html=commentdata['body_html'],
            lastchecked=datetime.utcnow(),
            lastmodified=datetime.utcnow()
        )

        # add to session and commit
        session.add(newcomment)
        session.commit()
