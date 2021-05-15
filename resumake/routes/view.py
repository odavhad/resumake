from json import loads
from urllib.parse import urlencode, urljoin

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from resumake.generate import get_tex_file
from resumake.hash import get_hash
from resumake.models import Config, General, User
from resumake.routes.auth import login_required
from resumake.settings import ENV_VAR

view_bp = Blueprint('view', __name__, url_prefix='/')


@view_bp.route('/general', methods=('GET', 'POST'))
@login_required
def general():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        website = request.form['website']
        linkedin = request.form['linkedin']
        summary = request.form['summary']

        user = User()
        gen = General(name, phone, email, website, linkedin, summary)

        user.update_general(gen.data)
        user.to_db()

        return redirect(url_for('view.general'))

    user = User()

    return render_template('view/general.html', gen=user.data['general'], data=user.data)


@view_bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        field = request.form['field']

        if field == 'edu':
            return redirect(url_for('add.education'))
        elif field == 'exp':
            return redirect(url_for('add.experience'))
        elif field == 'pro':
            return redirect(url_for('add.project'))
        elif field == 'pub':
            return redirect(url_for('add.publication'))

        return redirect(url_for('view.add'))

    user = User()

    return render_template('view/add.html', data=user.data)


@view_bp.route('/config', methods=('GET', 'POST'))
@login_required
def config():
    if request.method == 'POST':
        font = int(request.form['font'])
        horizontal = request.form['horizontal']
        vertical = request.form['vertical']

        user = User()
        conf = Config(font, horizontal, vertical)

        user.update_conf(conf.data)
        user.to_db()

        return redirect(url_for('view.config'))

    user = User()

    return render_template('view/config.html', conf=user.data['config'], data=user.data)


@view_bp.route('/education')
@login_required
def education():
    user = User()

    return render_template('view/education.html', edus=user.data['educations'], data=user.data)


@view_bp.route('/experience')
@login_required
def experience():
    user = User()

    return render_template('view/experience.html', exps=user.data['experiences'], data=user.data)


@view_bp.route('/project')
@login_required
def project():
    user = User()

    return render_template('view/project.html', pros=user.data['projects'], data=user.data)


@view_bp.route('/publication')
@login_required
def publication():
    user = User()

    return render_template('view/publication.html', pubs=user.data['publications'], data=user.data)


@view_bp.route('/skills', methods=('GET', 'POST'))
@login_required
def skills():
    if request.method == 'POST':
        skill = request.form['skill']

        user = User()

        user.add_skill(skill)
        user.to_db()

        return redirect(url_for('view.skills'))

    user = User()

    return render_template('view/skills.html', skills=user.data['skills'], data=user.data)


@view_bp.route('/raw/<filename>')
@login_required
def raw_data(filename):
    with open('instance/texfiles/{}.txt'.format(filename), 'r') as file:
        text = file.read()

    file.close()

    return render_template('file.html', content=text)


@view_bp.route('generate')
@login_required
def generate():
    user = User()
    if user.data['general'] == None:
        return redirect(url_for('view.general'))

    get_tex_file()

    param = {
        'url': urljoin(
            ENV_VAR['BASE_URL'],
            url_for('view.raw_data', filename=get_hash(session.get('user_id')))
        )
    }

    compile_base = "https://latexonline.cc/compile?"

    url = compile_base + urlencode(param)

    return redirect(url)
