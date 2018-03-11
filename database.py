from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

Base = declarative_base()
articles_tags = db.Table('articles_tags',db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),db.Column('article_id', db.Integer, db.ForeignKey('articles.id')))


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    summary = db.Column(db.String(300))
    content = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag',secondary=articles_tags,backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, summary, content, pub_time=None):
        self.title = title
        self.summary = summary
        self.content = content
        if pub_time:
            self.pub_time = pub_time

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


def _get_tag(name):
    name = name.lower()
    tag = db.session.query(Tag).filter(Tag.name==name).first()
    if not tag:
        tag = Tag(name)
        tag.save()
    return tag


def create_article(title, summary, content, pub_time=None, tagnames=[]):
    article = Article(title, summary, content, pub_time)
    for tagname in tagnames:
        tag = _get_tag(tagname.lower())
        article.tags.append(tag)
    article.save()
return article

SQLALCHEMY_DATABASE_URI = '"sqlite:///diary.db'
Base.metadata.create_all(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
