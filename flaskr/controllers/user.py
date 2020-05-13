from .. import app
from .. import jsonify
from .. import request


@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    Users controller entry point
    Handle user create or index action due to REST
    Return the response
    """
    pass
