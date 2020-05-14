from .. import mongo
from .. import base64
from .. import cv2
from .. import np
from .. import face_recognition


def create(data):
    """
    Try to create user with image encodings
    """
    # Get request data
    info = data.get('info')
    images = data.get('images')

    # FInd the existing user in the database
    user = mongo.db.users.find_one({'info': info})

    # Throw the error if user has already exist
    if user:
        raise ValueError('User already exists')

    image_encodings = []

    # Loop through inages and encode each to vector
    # Each encoded image append to image_encodings
    for image_str in images:
    	# Decode base64 image string to binary
        base64_decoded_image = base64.b64decode(image_str)

        # Cast image binary to numpy uint8 nd array
        image_array = np.fromstring(base64_decoded_image, np.uint8)

        # Create new image based on array
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Detect faces on the image
        faces = face_recognition.face_locations(image, model='hog')

        if len(faces) != 1:
            print(len(faces))
            raise ValueError('Invalid number of faces recognized. Needs 1')

        # Encode image face to vector
        face_image_encoding = face_recognition.face_encodings(image, faces)[0]

        image_encodings.append(face_image_encoding.tolist())

    # If all ok then create new user and save him
    user = {
        'info': info,
        'image_encodings': image_encodings
    }

    mongo.db.users.insert(user)

    user['id'] = str(user.get('_id'))
    del user['_id']

    return user