import os
from flask.globals import session
from flask import render_template

from resumake.models import User
from resumake.hash import get_hash


def get_tex_path():
    TEX_PATH = os.path.join(
        os.getcwd(),
        'resumake/static/tex'
    )

    return TEX_PATH


def get_path(filename):
    return os.path.join(
        get_tex_path(),
        filename
    )


def get_link(link):
    string = "}{link"

    return link + string


def get_header(data):
    header_file = get_path('header.txt')

    with open(header_file, 'r') as file:
        text = file.read()

    file.close()

    text = text.replace('{FONTSIZE}', str(data['fontsize']))
    text = text.replace('{LEFT}', str(data['margin']['left']))
    text = text.replace('{TOP}', str(data['margin']['top']))

    return text


def get_general(data):
    if data is None:
        return ""

    general_file = get_path('general.txt')

    with open(general_file, 'r') as file:
        text = file.read()

    file.close()

    text = text.replace('{NAME}', str(data['name']))
    text = text.replace('{PHONE}', str(data['phone']))
    text = text.replace('{EMAIL}', str(data['email']))
    text = text.replace('{WEBSITE}', str(data['website']))
    text = text.replace(
        '{LINKEDIN}',
        "https://www.linkedin.com/" + str(data['linkedin'])
    )
    text = text.replace('{SUMMARY}', str(data['summary']))

    return text


def get_education(data):
    edu_header_file = get_path('edu_header.txt')

    with open(edu_header_file, 'r') as file:
        text = file.read()

    file.close()

    edu_section1_file = get_path('edu_section1.txt')
    end_section = get_path('end_section.txt')
    des_file = get_path('des_point.txt')

    for edu in data:
        with open(edu_section1_file, 'r') as file:
            temp = file.read()

        file.close()

        temp = temp.replace('{SCHOOL}', str(edu['institute']))
        temp = temp.replace('{START}', str(edu['start']))
        temp = temp.replace('{END}', str(edu['end']))
        temp = temp.replace('{TITLE}', str(edu['title']))

        if edu['description'] != None:
            for des in edu['description']:
                with open(des_file, 'r') as file:
                    point = file.read()

                file.close()

                point = point.replace('{POINT}', des)

                temp += point

        with open(end_section, 'r') as file:
            temp += file.read()

        file.close()

        text += temp

    return text


def get_experience(data):
    exp_header_file = get_path('exp_header.txt')

    with open(exp_header_file, 'r') as file:
        text = file.read()

    file.close()

    exp_section1_file = get_path('exp_section1.txt')
    end_section = get_path('end_section.txt')
    des_file = get_path('des_point.txt')

    for exp in data:
        with open(exp_section1_file, 'r') as file:
            temp = file.read()

        file.close()

        temp = temp.replace('{WORKPLACE}', str(exp['workplace']))
        temp = temp.replace('{START}', str(exp['start']))
        temp = temp.replace('{END}', str(exp['end']))
        temp = temp.replace('{TITLE}', str(exp['title']))

        if exp['description'] != None:
            for des in exp['description']:
                with open(des_file, 'r') as file:
                    point = file.read()

                file.close()

                point = point.replace('{POINT}', des)

                temp += point

        with open(end_section, 'r') as file:
            temp += file.read()

        file.close()

        text += temp

    return text


def get_project(data):
    pro_header_file = get_path('pro_header.txt')

    with open(pro_header_file, 'r') as file:
        text = file.read()

    file.close()

    pro_section1_file = get_path('pro_section1.txt')
    end_section = get_path('end_section.txt')
    des_file = get_path('des_point.txt')

    for pro in data:
        with open(pro_section1_file, 'r') as file:
            temp = file.read()

        file.close()

        temp = temp.replace('{TITLE}', str(pro['title']))
        temp = temp.replace('{START}', str(pro['start']))
        temp = temp.replace('{END}', str(pro['end']))
        temp = temp.replace('{SUBTITLE}', str(pro['subtitle']))
        temp = temp.replace('{LINK}', get_link(pro['link']))

        if pro['description'] != None:
            for des in pro['description']:
                with open(des_file, 'r') as file:
                    point = file.read()

                file.close()

                point = point.replace('{POINT}', des)

                temp += point

        with open(end_section, 'r') as file:
            temp += file.read()

        file.close()

        text += temp

    return text


def get_publication(data):
    pub_header_file = get_path('pub_header.txt')

    with open(pub_header_file, 'r') as file:
        text = file.read()

    file.close()

    pub_section1_file = get_path('pub_section1.txt')

    for pub in data:
        with open(pub_section1_file, 'r') as file:
            temp = file.read()

        file.close()

        temp = temp.replace('{TITLE}', str(pub['title']))
        temp = temp.replace('{DATE}', str(pub['date']))
        temp = temp.replace('{JOURNAL}', str(pub['journal']))
        temp = temp.replace('{LINK}', get_link(pub['link']))

        text += temp

    return text


def get_skill(data):
    skill_file = get_path('skill.txt')

    with open(skill_file, 'r') as file:
        text = file.read()

    file.close()

    skill_string = ""
    for i in range(len(data) - 1):
        skill_string += data[i] + ', '

    skill_string += data[len(data) - 1]

    text = text.replace('{SKILLS}', skill_string)

    return text


def get_footer():
    footer_file = get_path('footer.txt')

    with open(footer_file, 'r') as file:
        text = file.read()

    file.close()

    return text


def get_tex_file():
    try:
        os.mkdir('instance/texfiles')
    except OSError:
        pass

    user = User()

    text = get_header(user.data['config'])
    text += get_general(user.data['general'])
    text += get_education(user.data['educations'])
    text += get_experience(user.data['experiences'])
    text += get_project(user.data['projects'])
    text += get_publication(user.data['publications'])
    text += get_skill(user.data['skills'])
    text += get_footer()

    with open('instance/texfiles/{}.txt'.format(get_hash(session.get('user_id'))), 'w') as file:
        file.write(text)

    file.close()
