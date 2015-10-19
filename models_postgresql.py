from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Subreddit(Base):
    __tablename__ = 'tblSubreddits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)


class Post(Base):
    __tablename__ = 'tblPosts'

    id = Column(Integer, primary_key=True)
    thread_id = Column(String, nullable=False)
    created_utc = Column(String, nullable=False)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    domain = Column(Integer, ForeignKey('tblSubreddits.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    score = Column(Integer, nullable=False)
    comments = Column(Integer, nullable=False)
    link_flair_text = Column(String, nullable=False)
    upvote_ratio = Column(Integer, nullable=False)
    permalink = Column(String, nullable=False)
    selftext = Column(String, nullable=False)
    selftext_html = Column(String, nullable=False)


class Comment(Base):
    __tablename__ = 'tblComments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('tblPosts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_utc = Column(String, nullable=False)
    author = Column(String, nullable=False)
    body = Column(String, nullable=False)
    body_html = Column(String, nullable=False)


class Message(Base):
    __tablename__ = 'tblMessages'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)


class MessageLog(Base):
    __tablename__ = 'tblMessageLog'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    executed = Column(DateTime, nullable=False)