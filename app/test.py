#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, filterprofile
from models import Settings
from twitter.models import User, Status
from datetime import datetime

settings = db.session.query(Settings).all()

#test:

#profile.description
#profile.followers_count
#profile.location
#profile.statuses_count
# 0, 6, 12, 24 months
#created = datetime.datetime.strptime(profile.created_at, "%a %b %d %H:%M:%S %z %Y")
#months = relativedelta(datetime.datetime.now(datetime.timezone.utc), created).years * 12
#lasttweetmonths = 

confs = {'description': [None, 'Trololo', 'Ololo', 'Simple description', 'den, prospect Wishful'],
         'followers_count': [None, 0, 1, 100, 1500],
         'location': [None, ['Russia',], ['Argentina',], ['Uruguay', 'Paraguay'], ['Germany', 'France']],
         'statuses_count': [None, 0, 1, 100, 1500],
         'created_at': [None, "Wed May 02 00:47:05 +0000 2012", "Wed May 02 00:47:05 +0000 2016", "Wed May 02 00:47:05 +0000 2018", "Mon Sep 03 00:47:05 +0000 2018"],
         'profile.status.created_at': [None, "Wed May 02 00:47:05 +0000 2012", "Wed May 02 00:47:05 +0000 2016", "Wed May 02 00:47:05 +0000 2018", "Mon Sep 03 00:47:05 +0000 2018"]
}

profiles = []
for i in range(5):
    np = User()
    np.id='user%s'%i
    np.screen_name = 'username%s'%i
    for c in confs:
        if c == 'description':
            np.description = confs[c][i]
        elif c == 'followers_count':
            np.followers_count = confs[c][i]
        elif c == 'location':
            np.location = confs[c][i]
        elif c == 'statuses_count':
            np.statuses_count = confs[c][i]
        elif c == 'created_at':
            np.created_at = confs[c][i]
        elif c == 'profile.status.created_at':
            ns = Status()
            ns.created_at = confs[c][i]
            ns.text = 'text'
            np.status = ns
    profiles.append(np)

print(profiles)
for s in settings:
    for p in profiles:
        filterprofile(p, s)
