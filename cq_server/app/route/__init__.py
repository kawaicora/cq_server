import socket
from flask import *



bp = Blueprint('root', __name__)



@bp.route('/<path:url_path>',methods=['GET','POST'])
def last_roue(url_path):

    # return render_template('error.html',error_obj=error_obj)
    return Response(json.dumps({"code":-1}), status=404, content_type='application/json')

# 注册服务

import app.route.cq_service