import io
import json
import array
import traceback
import zipfile

import music21
from musicsynthesisfinal import classical, pop, folk, hiphop

from flask import send_from_directory, Blueprint, request, make_response, send_file

bp = Blueprint('mydefault', __name__, url_prefix='/')


@bp.post("/api/generate")
def generate():
    data = json.loads(request.data)
    tone = data["tone"]
    style = str(data["style"])
    variant = None
    if "::" in style:
        (style, variant) = style.split("::", maxsplit=1)
    try:
        match style:
            case 'classical':
                stream = get_stream(classical.Classical(tone=tone, style=variant))
            case 'pop':
                stream = get_stream(pop.Pop(tone=tone))
            case 'folk':
                stream = get_stream(folk.Folk(tone=tone))
            case 'hiphop':
                stream = get_stream(hiphop.Hiphop(tone=tone, style=variant))
            case _:
                error = {
                    "success": False,
                    "err": {
                        "msg": "Fail to generate music: unknown style",
                        "detail": f"style {style}::{variant if variant is not None else ''} is unknown"
                    }
                }
                resp = make_response(json.dumps(error), 400)
                return resp
    except Exception as ex:
        error = {
            "success": False,
            "err": {
                "msg": "Fail to generate music",
                "detail": traceback.format_exception(type(ex), ex, ex.__traceback__)
            }
        }
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        resp = make_response(json.dumps(error), 400)
        return resp
    music_xml = music21.converter.toData(stream, 'musicxml')
    midi = music21.converter.toData(stream, 'midi')
    zip_buf = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buf, "w",
                         zipfile.ZIP_DEFLATED, False)
    zip_file.writestr("music.xml", music_xml)
    zip_file.writestr("music.midi", midi)
    zip_file.close()
    send_buf = io.BytesIO(zip_buf.getvalue())
    return send_file(send_buf, download_name="music.zip")


@bp.route("/")
def index():
    return send_from_directory('../../web/build', "index.html")


@bp.route("/<path:path>")
def base(path):
    return send_from_directory('../../web/build', path)


def get_stream(style):
    p = style.generate_music()
    ret = music21.stream.Stream()
    for pt in p:
        ret.insert(0, pt)
    return ret
