from .. import app
from .. import jsonify
from .. import capture_create_schema 
from .. import capture_service
from .. import validate_schema
from .. import validate_json
from .. import request


@app.route('/captures', methods=['GET'])
def index_captures():
    """
    The controller for captures
    Capture is the record that creates
    when some from existing users was reco-
    gnized
    Return the response
    """
    pass


@app.route('/captures', methods=['POST'])
# @validate_json
# @validate_schema(capture_create_schema)
def create_capture():
    """
    The controller for captures
    Capture is the record that creates
    when some from existing users was reco-
    gnized
    Return the response
    """
    app.logger.info(f'Received create capture request from {request.remote_addr}')

    request_json = request.json

    response_data = capture_service.create(request_json)

    app.logger.info(f'Create capture request from {request.remote_addr} has been handled')

    return jsonify({
        'data': response_data,
        'status': True,
        'description': 'Capture has been created'
    })