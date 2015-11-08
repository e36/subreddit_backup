from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Subreddit(Base):
    __tablename__ = 'tblSubreddits'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    domain = Column(String(50), nullable=False)


class Post(Base):
    __tablename__ = 'tblPosts'

    id = Column(Integer, primary_key=True)
    thread_id = Column(String(50), nullable=False)
    created_utc = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    title = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)
    domain = Column(Integer, ForeignKey('tblSubreddits.id'), nullable=False)
    score = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)
    link_flair_text = Column(String(50), nullable=False)
    upvote_ratio = Column(Integer, nullable=False)
    permalink = Column(String(200), nullable=False)
    selftext = Column(Text, nullable=False)
    selftext_html = Column(Text, nullable=False)
    lastchecked = Column(DateTime, nullable=False)
    lastmodified = Column(DateTime, nullable=False)


class Comment(Base):
    __tablename__ = 'tblComments'

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('tblPosts.id'), nullable=False)
    name = Column(String(50), nullable=False)
    parent_id = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
    created_utc = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    body = Column(Text, nullable=False)
    body_html = Column(Text, nullable=False)
    lastchecked = Column(DateTime, nullable=False)
    lastmodified = Column(DateTime, nullable=False)


class Message(Base):
    __tablename__ = 'tblMessages'

    id = Column(Integer, primary_key=True)
    message = Column(String(50), nullable=False)
    created = Column(DateTime, nullable=False)


class MessageLog(Base):
    __tablename__ = 'tblMessageLog'

    id = Column(Integer, primary_key=True)
    message = Column(String(50), nullable=True)
    created = Column(DateTime, nullable=False)
    executed = Column(DateTime, nullable=False)


class History(Base):
    __tablename__ = 'tblHistory'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    finished = Column(DateTime)
    message = Column(String(250))
