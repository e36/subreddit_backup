from sqlalchemy import update, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.sql import select, insert, update
from datetime import datetime
from models_mysql import MessageLog, Message, Post, Subreddit, Comment, History
from collections import namedtuple


def insert_history(Session, message):
    """
    Inserts a message into tblHistory.
    :param Session: sqlalchemy Session object
    :param message: dict with message, created datetime, finished datetime
    :return: nothing
    """

    # create session
    session = Session()

    newhistory = History(
        message=message['message'],
        created=message['created'],
        finished=message['finished'],
        status=message['status']
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
        post.comments = post_data['comments']
        post.lastchecked = datetime.utcnow()
        post.lastmodified = datetime.utcnow()
        post.archived = post_data['archived']

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
            comments=post_data['comments'],
            link_flair_text=post_data['link_flair_text'],
            upvote_ratio=post_data['upvote_ratio'],
            permalink=post_data['permalink'],
            selftext=post_data['selftext'],
            selftext_html=post_data['selftext_html'],
            lastchecked=datetime.utcnow(),
            lastmodified=datetime.utcnow(),
            archived=post_data['archived']
        )

        # add to session
        session.add(p)
        session.commit()

        return p.id


def insert_comment_data(Session, commentdata, thread_id):
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
    comment = session.query(Comment).filter(Comment.name == commentdata['name']).first()

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
            link_id=thread_id,
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


def bulk_comment_insert(Session, commentdata, thread_id):
    """
    Bulk insert of multiple comments into the database for a given thread id (e.g. 117 not ew38xn)
    :param Session: sql alchemy session
    :param commentdata: list of comment dictionaries
    :param thread_id: thread id (e.g. 117 not ew38xn)
    :return:
    """

    # init db session
    session = Session()

    # iterate through all comments and add them to the session
    for comment in commentdata:
        newcomment = Comment(
                link_id=thread_id,
                name=comment['name'],
                parent_id=comment['parent_id'],
                score=comment['score'],
                created_utc=comment['created_utc'],
                author=comment['author'],
                body=comment['body'],
                body_html=comment['body_html'],
                lastchecked=datetime.utcnow(),
                lastmodified=datetime.utcnow()
        )

        # add to session and commit
        session.add(newcomment)

    # commit all changes
    session.commit()


def update_comment(Session, comment_data):
    """
    Updates a comment row.  Be sure to send all comment data, since there is no logic to determine what was updated.
    :param Session: sql alchemy session
    :param comment_data: a dict of all comment data
    :return:
    """

    session = Session()


def get_post_data_from_db(Session, thread_id):
    """
    Gets the thread data from the database.  Returns thread id, lastupdated, archived, numcomments
    :param Session: sqlalchemy session
    :param thread_id: thread ID for the thread
    :return: list of dicts(thread_id,lastupdated,archived,num_comments)
    """

    # establish database session
    session = Session()

    # query the thread
    thread = session.query(Post.thread_id, Post.comments, Post.lastchecked, Post.archived).filter(Post.thread_id == thread_id)

    # insert into a dictionary if the query returned anything, or return 0
    if hasattr(thread, 'thread_id'):
        retdata = dict(thread_id=thread.thread_id, comments=thread.comments, lastchecked=thread.lastchecked, archived=thread.archived)
    else:
        retdata = False

    return retdata


def check_post_table(Session, thread_id):
    """
    Checks the db to see if the thread is already in there.  IF it exists, then return the row number.  If not,
    return None
    :param Session: SQL Alchemy session
    :param thread_id: thread id (e.g. 'cxs83s')
    :return: db ID or None
    """

    # establish session
    session = Session()

    # query the db
    thread = session.query(Post.id).filter(Post.thread_id == thread_id).scalar()

    return thread


def check_comment_table(Session, comment_id):
    """
    Checks the db to see if the comment is already in there.  IF it exists, then return the row number.  If not,
    return None
    :param Session: SQL Alchemy session
    :param comment_id: comment id (e.g. 't1_cxs83s')
    :return: db ID or None
    """

    # establish session
    session = Session()

    # query the db
    comment = session.query(Comment.id).filter(Comment.name == comment_id).scalar()

    return comment


def get_comment_keys(Session, thread_id):
    """
    Returns a list of [row, name] for all comments under thread_id
    :param Session: sqlalchemy session
    :param thread_id: valid thread/post row id (e.g. 12, 567) NOT the reddit post id
    :return: a list of all comment [row, name]
    """

    session = Session()

    # init list to be returned
    retlist = []

    # init named tuple
    element = namedtuple('element', 'id, name')

    for q in session.query(Comment.id, Comment.name).filter(Comment.link_id == thread_id):
        retlist.append(element(q.id, q.name))

    return retlist