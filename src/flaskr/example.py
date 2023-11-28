from flask import send_from_directory, Blueprint

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route("/")
def index():
    return send_from_directory('../../web/build', "index.html")


@bp.route("/<path:path>")
def base(path):
    return send_from_directory('../../web/build', path)
