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
        for puser in userlist:
            user2project = User2Project(
                user_id=puser['userID'],
                project_id=project.id
            )
            try:
                db.session.add(user2project)
                db.session.commit()
            except Exception as e:
                return jsonify({
                }), 500
    except Exception as e:
        return jsonify({
        }), 500
    return jsonify({
    }), 200