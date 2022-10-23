import json
import flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from . import api
from energy_gym_server.exceptions import EnergyGymException, InvalidRequestException


@api.after_request
def response_format(response: flask.Response):
    body = response.json
    if not (isinstance(body, dict) and body.get('error', False)):
        response.data = json.dumps({'error': False, 'data': body})
    return response


@api.before_request
def json_chek():
    if flask.request.data and not flask.request.is_json:
        raise InvalidRequestException('Тело запроса должно быть в формате JSON')


@api.errorhandler(Exception)
def error_handle(error: Exception) -> flask.Response:
    handled = isinstance(error, (HTTPException, EnergyGymException, ValidationError))
    
    if isinstance(error, ValidationError):
        errors = list(error.errors())
        for e in errors:
            if e['type'] == 'value_error.missing':
                e['msg'] += f": {', '.join(e['loc'])}"
        error_message = ' | '.join(e['msg'] for e in errors)
    else:
        error_message = str(error)

    response = flask.jsonify(
        {
            'error': True,
            'error_type': type(error).__name__ if handled else 'UnhandledException',
            'error_message': error_message
        }
    )

    if isinstance(error, HTTPException):
        return response, error.code
    else:
        return response, 200 if handled else 500
