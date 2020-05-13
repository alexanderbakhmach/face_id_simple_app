from .. import app
from .. import jsonify


@app.route('/captures', methods=['GET'])
def captures():
    """
    The controller for captures
    Capture is the record that creates
    when some from existing users was reco-
    gnized
    Return the response
    """
    pass
