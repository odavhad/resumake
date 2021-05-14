from flask import Blueprint, redirect, url_for
from resumake.models import User
from resumake.routes.auth import login_required

remove_bp = Blueprint('remove', __name__, url_prefix='/remove')


@remove_bp.route('/education/<int:index>', methods=('GET', 'POST'))
@login_required
def education(index):
    user = User()

    user.remove_education(index)
    user.to_db()

    return redirect(url_for('view.education'))


@remove_bp.route('/experience/<int:index>', methods=('GET', 'POST'))
@login_required
def experience(index):
    user = User()

    user.remove_experience(index)
    user.to_db()

    return redirect(url_for('view.experience'))


@remove_bp.route('/project/<int:index>', methods=('GET', 'POST'))
@login_required
def project(index):
    user = User()

    user.remove_project(index)
    user.to_db()

    return redirect(url_for('view.project'))


@remove_bp.route('/publication/<int:index>', methods=('GET', 'POST'))
@login_required
def publication(index):
    user = User()

    user.remove_publication(index)
    user.to_db()

    return redirect(url_for('view.publication'))


@remove_bp.route('/skill/<int:index>', methods=('GET', 'POST'))
@login_required
def skill(index):
    user = User()

    user.removeSkill(index)
    user.to_db()

    return redirect(url_for('view.skills'))
