from .. import mongo
from .. import os
from .. import base64
from .. import cv2
from .. import np
from .. import face_recognition
from .. import app
from .. import CANONICAL_JSON_OPTIONS
from .. import SOURCE_FOLDER


def index(data):
    users = mongo.db.users.find()

    def serializer(user):
        user['id'] = str(user.get('_id'))
        del user['_id']

        return user

    return list(map(serializer, users))


def create(data):
    """
    Try to create user with image encodings
    """
    # Get request data
    info = data.get('info')
    images = data.get('images')

    # Find the existing user in the database
    user = mongo.db.users.find_one({'info': info})

    # Throw the error if user has already exist
    #if user:
    #    raise ValueError('User already exists')

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
            raise ValueError('Invalid number of faces recognized. Needs 1')

        # Encode image face to vector
        face_image_encoding = face_recognition.face_encodings(image, faces)[0]

        image_encodings.append(face_image_encoding.tolist())

    image_encoding_file_name = 'enc.npy'
    image_encoding_file_path = os.path.join(app.root_path, 
                                            SOURCE_FOLDER,  
                                            image_encoding_file_name)

    if not os.path.exists(image_encoding_file_path):
        image_start_index = 0
        image_end_index = len(image_encodings) - 1

        np.save(image_encoding_file_path, np.asarray(image_encodings), allow_pickle=True)

    else:
        total_image_encodings = np.load(image_encoding_file_path, allow_pickle=True)
        image_encodings_size = total_image_encodings.shape[0]

        image_start_index = image_encodings_size
        image_end_index = image_start_index + len(image_encodings)

        total_image_encodings = np.concatenate((total_image_encodings, image_encodings), 0)

        np.save(image_encoding_file_path, total_image_encodings, allow_pickle=True)

    # If all ok then create new user and save him
    user = {
        'info': info,
        'image_indexes': [image_start_index, image_end_index]
    }

    mongo.db.users.insert(user)

    user['id'] = str(user.get('_id'))
    del user['_id']

    return user