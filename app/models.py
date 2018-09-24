#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, validates
from sqlalchemy import ForeignKey, select, func
from app import db
from dateutil.relativedelta import relativedelta


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    settings = db.relationship("Settings", backref="project", cascade="all,delete", uselist=False)
    profiles = db.relationship("Profile", backref="project", cascade="all,delete", lazy='joined')
    scantasks = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text())

    @hybrid_property
    def count_high(self):
        return len([p for p in self.profiles if p.priority > 0])

    @hybrid_property
    def count_low(self):
        return len([p for p in self.profiles if p.priority < 0])

    @hybrid_property
    def count_unprocessed(self):
        return len([p for p in self.profiles if p.processed is False])

    @hybrid_property
    def count_crawls(self):
        #return len([p for p in self.profiles if p.processed is False])
        # TODO
        return self.scantasks

    
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    include_keywords = db.Column(db.Text())
    exclude = db.Column(db.Boolean, default=False)
    followers = db.Column(db.Integer)
    tweets  = db.Column(db.Integer)
    tweetsperyear = db.Column(db.Integer)
    notweetsfor = db.Column(db.Integer)
    fromcountries = db.Column(db.Text())

    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitterhandle = db.Column(db.String(600))
    twitterid = db.Column(db.Integer)
    name = db.Column(db.String(600))
    surname = db.Column(db.String(600))
    fullname = db.Column(db.String(600))
    bio = db.Column(db.Text())
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    created = db.Column(db.Date)
    location = db.Column(db.Text())
    link = db.Column(db.Text())
    picture = db.Column(db.Text())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    priority = db.Column(db.Integer, default=0)
    processed = db.Column(db.Boolean, default=False)
    archived = db.Column(db.Boolean, default=False)
    
    @hybrid_property
    def years_created(self):
        return relativedelta(datetime.datetime.now(), self.created).years

    @hybrid_property
    def picture_large(self):
        return self.picture.replace("_normal", "_400x400")

    
