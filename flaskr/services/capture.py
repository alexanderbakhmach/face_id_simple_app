from .. import face_recognition
from .. import mongo
from .. import np
from .. import DISTANCE
from .. import time

def create(data):
    description = data.get('description')
    image_encoding = data.get('image_encoding')
    now = time.time()
    capture_user = None
    users = mongo.db.users.find()

    for user in users:
        image_encodings = user.get('image_encodings')

        image_encodings_array = np.asarray([np.asarray(image_encoding) for image_encoding in image_encodings])

        image_encoding_array = np.asarray(image_encoding)

        distances = face_recognition.face_distance(image_encodings_array, image_encoding_array)

        if any(distance < DISTANCE for distance in distances):
            should_create = False

            user_id = user.get('_id')

            old_capture = mongo.db.captures.find_one({'user_id': user_id}, sort=[('created', -1)])

            if old_capture:
                old_capture_created = old_capture.get('created')
                time_delta = now - old_capture_created

                if time_delta > 30:
                    should_create = True

            else:
                should_create = True

            if should_create:
                capture_user = user
                break
    
    if capture_user:
        capture = {
            'description': description,
            'user_id': capture_user.get('_id'),
            'created': now
        }

        mongo.db.captures.insert(capture)

        capture['id'] = str(capture.pop('_id'))
        capture['user_id'] = str(capture.pop('user_id'))

        return capture

    else:
        return None