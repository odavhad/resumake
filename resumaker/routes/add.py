from flask import Blueprint, redirect, render_template, request, url_for
from resumaker.models import Education, Experience, Project, Publication, User
from resumaker.routes.auth import login_required

add_bp = Blueprint('add', __name__, url_prefix='/add')


@add_bp.route('/education', methods=('GET', "POST"))
@login_required
def education():
    if request.method == 'POST':
        institute = request.form.get('institute')
        title = request.form.get('title')
        start = request.form.get('start')
        end = request.form.get('end')
        description = request.form.get('description')

        user = User()
        edu = Education(institute, title, start, end, description)

        user.add_education(edu.data)
        user.to_db()

        return redirect(url_for('view.education'))

    user = User()

    return render_template('add/education.html', data=user.data)


@add_bp.route('/experience', methods=('GET', "POST"))
@login_required
def experience():
    if request.method == 'POST':
        workplace = request.form.get('workplace')
        title = request.form.get('title')
        start = request.form.get('start')
        end = request.form.get('end')
        description = request.form.get('description')

        user = User()
        exp = Experience(workplace, title, start, end, description)

        user.add_experience(exp.data)
        user.to_db()

        return redirect(url_for('view.experience'))

    user = User()

    return render_template('add/experience.html', data=user.data)


@add_bp.route('/project', methods=('GET', "POST"))
@login_required
def project():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        start = request.form.get('start')
        end = request.form.get('end')
        link = request.form.get('link')
        description = request.form.get('description')

        user = User()
        pro = Project(title, start, end, subtitle, link, description)

        user.add_project(pro.data)
        user.to_db()

        return redirect(url_for('view.project'))

    user = User()

    return render_template('add/project.html', data=user.data)


@add_bp.route('/publication', methods=('GET', "POST"))
@login_required
def publication():
    if request.method == 'POST':
        title = request.form.get('title')
        journal = request.form.get('journal')
        link = request.form.get('link')
        date = request.form.get('date')

        user = User()
        pub = Publication(title, date, journal, link)

        user.add_publication(pub.data)
        user.to_db()

        return redirect(url_for('view.publication'))

    user = User()

    return render_template('add/publication.html', data=user.data)
