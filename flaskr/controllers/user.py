from .. import app
from .. import jsonify
from .. import request
from .. import validate_json
from .. import validate_schema
from .. import user_create_schema
from .. import user_service


@app.route('/users', methods=['GET'])
def index_users():
    """
    Users controller entry point
    Handle user index action due to REST
    Return the response
    """
    app.logger.info(f'Received index users request from {request.remote_addr}')

    request_args = request.args

    response_data = user_service.index(request_args)

    app.logger.info(f'Index users request from {request.remote_addr} has been handled')

    return jsonify({
        'data': response_data,
        'status': True
    })


@app.route('/users', methods=['POST'])
@validate_json
@validate_schema(user_create_schema)
def create_user():
    """
    Users controller entry point
    Handle user create action due to REST
    Return the response
    """
    app.logger.info(f'Received create user request from {request.remote_addr}')

    request_json = request.json

    response_data = user_service.create(request_json)

    app.logger.info(f'Create user request from {request.remote_addr} has been handled')

    if response_data:
        return jsonify({
            'data': response_data,
            'status': True,
            'description': 'New capture was created'
        })

    else:
        return jsonify({
            'status': False,
            'description': 'New capture was not created'   
        })

