from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Team, Group, User, Project, Message, Statu, File, Comment, User2Project
from ..decorator import login_required
import time


@api.route('project/new/', methods=['POST'])
@login_required
def project_new(uid):
    username = request.get_json().get('username')
    projectname = request.get_json().get('projectname')
    userlist = request.get_json().get('userlist')
    intro = request.get_json().get('intro')

    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    count = len(userlist)
    user = User.query.filter_by(name=username).first()
    team_id = user.team_id

    project = Project(name=projectname,
                      intro=intro,
                      time=localtime,
                      count=count,
                      team_id=team_id)

    try:
        db.session.add(project)
        db.session.commit()
        user2project = User2Project(
            user_id=user.id,
            project_id=project.id
        )
        db.session.add(user2project)
        db.session.commit()
        for puser in userlist:
            user2project = User2Project(
                user_id=puser['userID'],
                project_id=project.id
            )
            db.session.add(user2project)
            db.session.commit()
    except Exception as e:
        return jsonify({
        }), 500
    return jsonify({
        'project_id': str(project.id)
    }), 200


@api.route('project/<int:pid>/', methods=['POST', 'DELETE'])
@login_required
def project_pid(uid, pid):
    if request.method == 'POST':
        intro = request.get_json().get('intro')
        name = request.get_json().get('name')

        try:
            project = Project.query.filter_by(id=pid).first()
            project.name = name
            project.intro = intro

            db.session.add(project)
            db.session.commit()
        except:
            return jsonify({
            }), 500
        return jsonify({
        }), 200
    elif request.method == 'DELETE':
        try:
            project = Project.query.filter_by(id=pid).first()
            db.session.delete(project)
            db.session.commit()
            user2projects = User2Project.query.filter_by(project_id=pid)
            for u2p in user2projects:
                db.session.delete(u2p)
            db.session.commit()
            files = File.query.filter_by(project_id=pid)
            for file in files:
                db.session.delete(file)
            db.session.commit()
        except:
            return jsonify({
            }), 500
        return jsonify({
        }), 200
    else:
        return jsonify({
        }), 405