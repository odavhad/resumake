from json import loads, dumps

from flask.globals import session

from .db import get_db

def formatDate(date):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    year, month, day = tuple(map(int, date.split('-')))

    date = "{} {}".format(months[month - 1], year)

    return date

def formatDescription(description):
    return description

class General(object):
    data = dict()

    def __init__(self, name, phone, email, website=None, linkedin=None):
        self.data['name'] = name
        self.data['phone'] = phone
        self.data['email'] = email
        self.data['website'] = website
        self.data['linkedin'] = linkedin

class Education(object):
    data = dict()

    def __init__(self, institute, title, start, end, description):
        self.data['institute'] = institute
        self.data['title'] = title
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)
        self.data['description'] = formatDescription()

class Experience(object):
    data = dict()

    def __init__(self, workplace, title, start, end):
        self.data['workplace'] = workplace
        self.data['title'] = title
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)

class Project(object):
    data = dict()

    def __init__(self, title, start, end, subtitle=None, link=None):
        self.data['title'] = title
        self.data['subtitle'] = subtitle
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)
        self.data['link'] = link

class Publication(object):
    data = dict()

    def __init__(self, title, date, journal=None, link=None):
        self.data['title'] = title
        self.data['journal'] = journal
        self.data['date'] = formatDate(date)
        self.data['link'] = link    

class User(object):
    data = {
        'general': None,
        'educations': list(),
        'experiences': list(),
        'projects': list(),
        'publications': list(),
        'skills': list()
    }

    def __init__(self, signup=False):
        if signup is True:
            return

        id = session.get('user_id')
        db = get_db()

        self.data = loads(db.execute(
                        'SELECT resume_data FROM user WHERE id = ?', (id,)
                    ).fetchone()['resume_data'])
    
    def to_db(self):
        id = session.get('user_id')
        db = get_db()

        db.execute(
            'UPDATE user SET resume_data = ? WHERE id = ?', (dumps(self.data), id)
        )
        db.commit()

    def add_skill(self, skill):
        self.data['skills'].append(skill)

    def update_general(self, general):
        self.data['general'] = general
    
    def add_education(self, education):
        self.data['educations'].append(education)

    def add_experience(self, experience):
        self.data['experiences'].append(experience)
    
    def add_project(self, project):
        self.data['projects'].append(project)
    
    def add_publication(self, publication):
        self.data['publications'].append(publication)
