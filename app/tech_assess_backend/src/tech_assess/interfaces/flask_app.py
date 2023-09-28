from tech_assess.bootstrap import bootstrap
from tech_assess.domain import commands, errors
from tech_assess.service import queries
from tech_assess.config import get_file_storage_config
from tech_assess.logs import logger, log_request_time

import json
from flask import Flask, request, Response, abort, send_file
from flask_cors import CORS
from pydantic import ValidationError

app = Flask(__name__)
CORS(app)

bus = bootstrap()


@app.route("/", methods=['GET'])
def get_health():
    return Response("OK", status=200, mimetype="text/plain")


@app.route("/recordings", methods=['POST'])
@log_request_time
def post_recording():
    logger.info("request: post_recording")
    try:
        command = commands.CreateRecording.from_dict(request.files)
    except ValidationError as e:
        abort(400, str(e))

    try:
        bus.handle(command)
    except Exception as e:
        abort(500, str(e))

    result = queries.get_recording(recording_uuid=command.recording_uuid,
                                   uow=bus.uow)
    return Response(json.dumps(result),
                    status=201,
                    mimetype="application/json")


@app.route("/recordings/<uuid>", methods=['GET'])
def get_recording(uuid):
    logger.info("request: get_recording")
    result = queries.get_recording(recording_uuid=uuid, uow=bus.uow)
    return Response(json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route("/recordings/<uuid>/output", methods=['GET'])
def get_recording_output(uuid):
    logger.info("request: get_recording_output")
    result = queries.get_recording_output(recording_uuid=uuid, uow=bus.uow)

    return send_file(result)

