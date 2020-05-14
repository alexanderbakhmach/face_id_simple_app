from .. import app
from .. import jsonify 
from .. import ValidationError
from .. import BadRequest


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({
        'status': False,
        'description': str(e)
    }), 422


@app.errorhandler(ValidationError)
def handle_value_error(e):
    return jsonify({
        'status': False,
        'description': e.message
    }), 422


@app.errorhandler(BadRequest)
def handle_value_error(e):
    return jsonify({
        'status': False,
        'description': 'Payload must be a valid json'
    }), 422
