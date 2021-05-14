from json import dumps, loads

from flask.globals import session

from .db import get_db


def formatDate(date):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    year, month, day = tuple(map(int, date.split('-')))

    date = "{} {}".format(months[month - 1], year)

    return date


def formatDescription(description):
    if (len(description) == 0):
        return None

    return description.split('\r\n')


class Config(object):
    data = dict()

    def __init__(self, fontsize=11, horizontal=0.6, vertical=0.45):
        self.data['fontsize'] = fontsize
        self.data['margin'] = {
            'left': horizontal,
            'right': horizontal,
            'top': vertical,
            'bottom': vertical
        }


class General(object):
    data = dict()

    def __init__(self, name, phone, email, website=None, linkedin=None, summary=None):
        self.data['name'] = name
        self.data['phone'] = phone
        self.data['email'] = email
        self.data['website'] = website
        self.data['linkedin'] = linkedin
        self.data['summary'] = summary


class Education(object):
    data = dict()

    def __init__(self, institute, title, start, end, description=None):
        self.data['institute'] = institute
        self.data['title'] = title
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)
        self.data['description'] = formatDescription(description)


class Experience(object):
    data = dict()

    def __init__(self, workplace, title, start, end, description=None):
        self.data['workplace'] = workplace
        self.data['title'] = title
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)
        self.data['description'] = formatDescription(description)


class Project(object):
    data = dict()

    def __init__(self, title, start, end, subtitle=None, link=None, description=None):
        self.data['title'] = title
        self.data['subtitle'] = subtitle
        self.data['start'] = formatDate(start)
        self.data['end'] = formatDate(end)
        self.data['link'] = link
        self.data['description'] = formatDescription(description)


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
        'skills': list(),
        'config': None
    }

    def __init__(self, signup=False):
        config = Config()
        self.data['config'] = config.data

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
            'UPDATE user SET resume_data = ? WHERE id = ?', (dumps(
                self.data), id)
        )
        db.commit()

    def add_skill(self, skill):
        if skill not in self.data['skills']:
            self.data['skills'].append(skill)

    def removeSkill(self, index):
        self.data['skills'].pop(index)

    def update_conf(self, config):
        self.data['config'] = config

    def update_general(self, general):
        self.data['general'] = general

    def add_education(self, education):
        self.data['educations'].append(education)

    def remove_education(self, index):
        self.data['educations'].pop(index)

    def add_experience(self, experience):
        self.data['experiences'].append(experience)

    def remove_experience(self, index):
        self.data['experiences'].pop(index)

    def add_project(self, project):
        self.data['projects'].append(project)

    def remove_project(self, index):
        self.data['projects'].pop(index)

    def add_publication(self, publication):
        self.data['publications'].append(publication)

    def remove_publication(self, index):
        self.data['publications'].pop(index)
